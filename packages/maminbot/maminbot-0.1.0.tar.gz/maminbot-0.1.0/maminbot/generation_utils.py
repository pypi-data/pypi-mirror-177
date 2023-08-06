from torch import nn
from transformers.generation_logits_process import LogitsProcessorList
from transformers.generation_stopping_criteria import (
    StoppingCriteriaList,
    validate_stopping_criteria,
)
from transformers.generation_utils import GreedySearchEncoderDecoderOutput, \
    GreedySearchDecoderOnlyOutput, SampleEncoderDecoderOutput, \
    SampleDecoderOnlyOutput
from transformers.utils import logging
from typing import Iterable, List, Optional, Tuple, Union
import inspect
import torch
import torch.distributed as dist
import warnings

from htools import tolist


logger = logging.get_logger(__name__)
GreedySearchOutput = Union[GreedySearchEncoderDecoderOutput,
                           GreedySearchDecoderOnlyOutput]
SampleOutput = Union[SampleEncoderDecoderOutput, SampleDecoderOnlyOutput]
GenerateOutput = Union[GreedySearchOutput, SampleOutput]


def ids_to_pretty_tokens(tokenizer, ids):
    """Similar to tokenizer.decode but returns a list of strings rather than a
    single string. Similar to tokenizer.convert_ids_to_tokens but returns
    human-friendly tokens rather than machine-friendly (e.g. using actual
    spaces rather than some coded representation.)

    Parameters
    ----------
    tokenizer
    ids: list[int] or int

    Returns
    -------
    list[str]
    """
    return [tokenizer.convert_tokens_to_string(tok) for tok in
            tokenizer.convert_ids_to_tokens(tolist(ids))]


def _top_word_probs(probs, next_tokens, tokenizer, probs_per_token=5):
    """
    Returns
    -------
    tuple[str, dict]: String is next predicted token. w2p is a dict mapping
    token string to predicted probability.
    """
    topk = torch.topk(probs, probs_per_token)
    # Ensure actual sampled token is included.
    # Shape: (num_return_sequences, probs_per_word + 1)
    ids = torch.cat((next_tokens[:, None], topk.indices), -1)
    id_probs = torch.gather(probs, -1, ids)
    w2p = [dict(zip((ids_to_pretty_tokens(tokenizer, id_row)),
                    prob_row.tolist()))
           for id_row, prob_row in zip(ids, id_probs)]
    return ids_to_pretty_tokens(tokenizer, next_tokens), w2p


def live_greedy_search(
        model,
        tokenizer,
        input_ids: torch.LongTensor,
        logits_processor: Optional[LogitsProcessorList] = None,
        stopping_criteria: Optional[StoppingCriteriaList] = None,
        max_length: Optional[int] = None,
        pad_token_id: Optional[int] = None,
        eos_token_id: Optional[int] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        output_scores: Optional[bool] = None,
        return_dict_in_generate: Optional[bool] = None,
        synced_gpus: Optional[bool] = False,
        probs_per_token: Optional[int] = 5,
        **model_kwargs,
) -> Union[GreedySearchOutput, torch.LongTensor]:
    r"""
    Generates sequences of token ids for models with a language modeling head using **greedy decoding** and can be
    used for text-decoder, text-to-text, speech-to-text, and vision-to-text models.
    Parameters:
        input_ids (`torch.LongTensor` of shape `(batch_size, sequence_length)`):
            The sequence used as a prompt for the generation.
        logits_processor (`LogitsProcessorList`, *optional*):
            An instance of [`LogitsProcessorList`]. List of instances of class derived from [`LogitsProcessor`]
            used to modify the prediction scores of the language modeling head applied at each generation step.
        stopping_criteria (`StoppingCriteriaList`, *optional*):
            An instance of [`StoppingCriteriaList`]. List of instances of class derived from [`StoppingCriteria`]
            used to tell if the generation loop should stop.
        max_length (`int`, *optional*, defaults to 20):
            **DEPRECATED**. Use `logits_processor` or `stopping_criteria` directly to cap the number of generated
            tokens. The maximum length of the sequence to be generated.
        pad_token_id (`int`, *optional*):
            The id of the *padding* token.
        eos_token_id (`int`, *optional*):
            The id of the *end-of-sequence* token.
        output_attentions (`bool`, *optional*, defaults to `False`):
            Whether or not to return the attentions tensors of all attention layers. See `attentions` under
            returned tensors for more details.
        output_hidden_states (`bool`, *optional*, defaults to `False`):
            Whether or not to return the hidden states of all layers. See `hidden_states` under returned tensors
            for more details.
        output_scores (`bool`, *optional*, defaults to `False`):
            Whether or not to return the prediction scores. See `scores` under returned tensors for more details.
        return_dict_in_generate (`bool`, *optional*, defaults to `False`):
            Whether or not to return a [`~utils.ModelOutput`] instead of a plain tuple.
        synced_gpus (`bool`, *optional*, defaults to `False`):
            Whether to continue running the while loop until max_length (needed for ZeRO stage 3)
        model_kwargs:
            Additional model specific keyword arguments will be forwarded to the `forward` function of the model.
            If model is an encoder-decoder model the kwargs should include `encoder_outputs`.

    Yields
    ------
    tuple[list[str], list[dict], list[int]]
    """
    # init values
    logits_processor = (logits_processor if logits_processor is not None
                        else LogitsProcessorList())
    stopping_criteria = (stopping_criteria if stopping_criteria is not None
                         else StoppingCriteriaList())
    if max_length is not None:
        warnings.warn(
            "`max_length` is deprecated in this function, use "
            "`stopping_criteria=StoppingCriteriaList("
            "[MaxLengthCriteria(max_length=max_length)])` instead.",
            UserWarning,
        )
        stopping_criteria = validate_stopping_criteria(stopping_criteria,
                                                       max_length)
    pad_token_id = (pad_token_id if pad_token_id is not None
                    else model.config.pad_token_id)
    eos_token_id = (eos_token_id if eos_token_id is not None
                    else model.config.eos_token_id)
    output_scores = (output_scores if output_scores is not None
                     else model.config.output_scores)
    output_attentions = (output_attentions if output_attentions is not None
                         else model.config.output_attentions)
    output_hidden_states = (
        output_hidden_states if output_hidden_states
        is not None else model.config.output_hidden_states
    )
    return_dict_in_generate = (
        return_dict_in_generate if return_dict_in_generate
        is not None else model.config.return_dict_in_generate
    )

    # init attention / hidden states / scores tuples
    scores = () if (return_dict_in_generate and output_scores) else None
    decoder_attentions = () if (
                return_dict_in_generate and output_attentions) else None
    cross_attentions = () if (
                return_dict_in_generate and output_attentions) else None
    decoder_hidden_states = () if (
                return_dict_in_generate and output_hidden_states) else None

    # If model is an encoder-decoder, retrieve encoder attention weights and
    # hidden states.
    if return_dict_in_generate and model.config.is_encoder_decoder:
        encoder_attentions = model_kwargs["encoder_outputs"].get(
            "attentions") if output_attentions else None
        encoder_hidden_states = (
            model_kwargs["encoder_outputs"].get(
                "hidden_states") if output_hidden_states else None
        )

    # Keep track of which sequences are already finished.
    unfinished_sequences = input_ids.new(input_ids.shape[0]).fill_(1)
    cur_len = input_ids.shape[-1]

    this_peer_finished = False  # used by synced_gpus only
    while True:

        if synced_gpus:
            # Under synced_gpus the `forward` call must continue until all
            # gpus complete their sequence. The following logic allows an early
            # break if all peers finished generating their sequence
            this_peer_finished_flag = torch.tensor(
                0.0 if this_peer_finished else 1.0).to(input_ids.device)
            # send 0.0 if we finished, 1.0 otherwise
            dist.all_reduce(this_peer_finished_flag, op=dist.ReduceOp.SUM)
            # did all peers finish? the reduced sum will be 0.0 then
            if this_peer_finished_flag.item() == 0.0:
                break

        # prepare model inputs
        model_inputs = model.prepare_inputs_for_generation(input_ids,
                                                           **model_kwargs)

        # forward pass to get next token
        outputs = model(
            **model_inputs,
            return_dict=True,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
        )

        # Don't waste resources running the code we don't need.
        if synced_gpus and this_peer_finished:
            cur_len = cur_len + 1
            continue

        next_token_logits = outputs.logits[:, -1, :]

        # Store scores, attentions and hidden_states when required.
        if return_dict_in_generate:
            if output_scores:
                scores += (next_token_logits,)
            if output_attentions:
                decoder_attentions += (
                    (outputs.decoder_attentions,)
                    if model.config.is_encoder_decoder else (
                    outputs.attentions,)
                )
                if model.config.is_encoder_decoder:
                    cross_attentions += (outputs.cross_attentions,)

            if output_hidden_states:
                decoder_hidden_states += (
                    (outputs.decoder_hidden_states,)
                    if model.config.is_encoder_decoder
                    else (outputs.hidden_states,)
                )

        # pre-process distribution
        next_tokens_scores = logits_processor(input_ids, next_token_logits)

        # argmax
        next_tokens = torch.argmax(next_tokens_scores, dim=-1)

        # finished sentences should have their next token be a padding token
        if eos_token_id is not None:
            if pad_token_id is None:
                raise ValueError(
                    "If `eos_token_id` is defined, make sure that "
                    "`pad_token_id` is defined."
                )
            next_tokens = next_tokens * unfinished_sequences + pad_token_id * (
                        1 - unfinished_sequences)

        probs = nn.functional.softmax(next_tokens_scores, dim=-1)

        # Compute items to yield now, but wait until `unfinished_sequences` is
        # updated several lines below before yielding. Huggingface sets
        # corresponding unfinished_sequences val to 0 on the token AFTER
        # EOS_TOKEN, but we want it to be 0 starting WITH that token. Don't
        # compute earlier because we want to wait for next_tokens to be updated
        # first (sets finished sequence predictions to EOS) and don't do this
        # later in case any of the _top_word_probs inputs change (don't
        # think they do, but just being careful).
        next_toks, next_w2ps =_top_word_probs(probs, next_tokens,
                                              tokenizer, probs_per_token)

        # update generated ids, model inputs, and length for next step
        input_ids = torch.cat([input_ids, next_tokens[:, None]], dim=-1)
        model_kwargs = model._update_model_kwargs_for_generation(
            outputs, model_kwargs,
            is_encoder_decoder=model.config.is_encoder_decoder
        )
        cur_len = cur_len + 1

        # if eos_token was found in one sentence, set sentence to finished
        if eos_token_id is not None:
            unfinished_sequences = unfinished_sequences.mul(
                (next_tokens != eos_token_id).long())

        yield next_toks, next_w2ps, unfinished_sequences.tolist()

        # Stop when each sentence is finished, or if we exceed the max length.
        if unfinished_sequences.max() == 0 or stopping_criteria(input_ids,
                                                                scores):
            if not synced_gpus:
                break
            else:
                this_peer_finished = True


# Note: originally tried subclassing GenerationMixin but then we'd have to
# redefine a bunch of intermediate classes OR somehow change an object
# parent class at runtime via python dark arts. Decided to just leave these
# as functions.
def live_sample(
        model,
        tokenizer,
        input_ids: torch.LongTensor,
        logits_processor: Optional[LogitsProcessorList] = None,
        stopping_criteria: Optional[StoppingCriteriaList] = None,
        logits_warper: Optional[LogitsProcessorList] = None,
        max_length: Optional[int] = None,
        pad_token_id: Optional[int] = None,
        eos_token_id: Optional[int] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        output_scores: Optional[bool] = None,
        return_dict_in_generate: Optional[bool] = None,
        synced_gpus: Optional[bool] = False,
        probs_per_token: Optional[int] = 5,
        **model_kwargs,
) -> Union[SampleOutput, torch.LongTensor]:
    r"""
    Generates sequences of token ids for models with a language modeling head using **multinomial sampling** and
    can be used for text-decoder, text-to-text, speech-to-text, and vision-to-text models.
    Parameters:
        input_ids (`torch.LongTensor` of shape `(batch_size, sequence_length)`):
            The sequence used as a prompt for the generation.
        logits_processor (`LogitsProcessorList`, *optional*):
            An instance of [`LogitsProcessorList`]. List of instances of class derived from [`LogitsProcessor`]
            used to modify the prediction scores of the language modeling head applied at each generation step.
        stopping_criteria (`StoppingCriteriaList`, *optional*):
            An instance of [`StoppingCriteriaList`]. List of instances of class derived from [`StoppingCriteria`]
            used to tell if the generation loop should stop.
        logits_warper (`LogitsProcessorList`, *optional*):
            An instance of [`LogitsProcessorList`]. List of instances of class derived from [`LogitsWarper`] used
            to warp the prediction score distribution of the language modeling head applied before multinomial
            sampling at each generation step.
        max_length (`int`, *optional*, defaults to 20):
            **DEPRECATED**. Use `logits_processor` or `stopping_criteria` directly to cap the number of generated
            tokens. The maximum length of the sequence to be generated.
        pad_token_id (`int`, *optional*):
            The id of the *padding* token.
        eos_token_id (`int`, *optional*):
            The id of the *end-of-sequence* token.
        output_attentions (`bool`, *optional*, defaults to `False`):
            Whether or not to return the attentions tensors of all attention layers. See `attentions` under
            returned tensors for more details.
        output_hidden_states (`bool`, *optional*, defaults to `False`):
            Whether or not to return the hidden states of all layers. See `hidden_states` under returned tensors
            for more details.
        output_scores (`bool`, *optional*, defaults to `False`):
            Whether or not to return the prediction scores. See `scores` under returned tensors for more details.
        return_dict_in_generate (`bool`, *optional*, defaults to `False`):
            Whether or not to return a [`~utils.ModelOutput`] instead of a plain tuple.
        synced_gpus (`bool`, *optional*, defaults to `False`):
            Whether to continue running the while loop until max_length (needed for ZeRO stage 3)
        model_kwargs:
            Additional model specific kwargs will be forwarded to the `forward` function of the model. If model is
            an encoder-decoder model the kwargs should include `encoder_outputs`.

    Yields
    ------
    tuple[list[str], list[dict], list[int]]
    """
    # init values
    logits_processor = (logits_processor if logits_processor is not None
                        else LogitsProcessorList())
    stopping_criteria = (stopping_criteria if stopping_criteria is not None
                         else StoppingCriteriaList())
    if max_length is not None:
        warnings.warn(
            "`max_length` is deprecated in this function, use"
            " `stopping_criteria=StoppingCriteriaList("
            "MaxLengthCriteria(max_length=max_length))` instead.",
            UserWarning,
        )
        stopping_criteria = validate_stopping_criteria(stopping_criteria,
                                                       max_length)
    logits_warper = (logits_warper if logits_warper is not None
                     else LogitsProcessorList())
    pad_token_id = (pad_token_id if pad_token_id is not None
                    else model.config.pad_token_id)
    eos_token_id = (eos_token_id if eos_token_id is not None
                    else model.config.eos_token_id)
    output_scores = (output_scores if output_scores is not None
                     else model.config.output_scores)
    output_attentions = (output_attentions if output_attentions is not None
                         else model.config.output_attentions)
    output_hidden_states = (
        output_hidden_states if output_hidden_states is not None
        else model.config.output_hidden_states
    )
    return_dict_in_generate = (
        return_dict_in_generate if return_dict_in_generate is not None
        else model.config.return_dict_in_generate
    )

    # init attention / hidden states / scores tuples
    scores = () if (return_dict_in_generate and output_scores) else None
    decoder_attentions = () if (
                return_dict_in_generate and output_attentions) else None
    cross_attentions = () if (
                return_dict_in_generate and output_attentions) else None
    decoder_hidden_states = () if (
                return_dict_in_generate and output_hidden_states) else None

    # If model is an encoder-decoder, retrieve encoder attention weights and
    # hidden states.
    if return_dict_in_generate and model.config.is_encoder_decoder:
        encoder_attentions = model_kwargs["encoder_outputs"].get(
            "attentions") if output_attentions else None
        encoder_hidden_states = (
            model_kwargs["encoder_outputs"].get(
                "hidden_states") if output_hidden_states else None
        )

    # keep track of which sequences are already finished
    unfinished_sequences = input_ids.new(input_ids.shape[0]).fill_(1)

    this_peer_finished = False  # used by synced_gpus only
    # auto-regressive generation
    while True:
        if synced_gpus:
            # Under synced_gpus the `forward` call must continue until all
            # gpus complete their sequence. The following logic allows an early
            # break if all peers finished generating their sequence
            this_peer_finished_flag = torch.tensor(
                0.0 if this_peer_finished else 1.0).to(input_ids.device)
            # send 0.0 if we finished, 1.0 otherwise
            dist.all_reduce(this_peer_finished_flag, op=dist.ReduceOp.SUM)
            # did all peers finish? the reduced sum will be 0.0 then
            if this_peer_finished_flag.item() == 0.0:
                break

        # prepare model inputs
        model_inputs = model.prepare_inputs_for_generation(input_ids,
                                                           **model_kwargs)

        # forward pass to get next token
        outputs = model(
            **model_inputs,
            return_dict=True,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
        )

        if synced_gpus and this_peer_finished:
            continue  # don't waste resources running the code we don't need

        next_token_logits = outputs.logits[:, -1, :]

        # pre-process distribution
        next_token_scores = logits_processor(input_ids, next_token_logits)
        next_token_scores = logits_warper(input_ids, next_token_scores)

        # Store scores, attentions and hidden_states when required
        if return_dict_in_generate:
            if output_scores:
                scores += (next_token_scores,)
            if output_attentions:
                decoder_attentions += (
                    (outputs.decoder_attentions,)
                    if model.config.is_encoder_decoder else
                    (outputs.attentions,)
                )
                if model.config.is_encoder_decoder:
                    cross_attentions += (outputs.cross_attentions,)

            if output_hidden_states:
                decoder_hidden_states += (
                    (outputs.decoder_hidden_states,)
                    if model.config.is_encoder_decoder
                    else (outputs.hidden_states,)
                )

        # sample
        # Shape: (num_return_sequences, vocab_size)
        probs = nn.functional.softmax(next_token_scores, dim=-1)
        # Shape: (num_return_sequences,)
        next_tokens = torch.multinomial(probs, num_samples=1).squeeze(1)

        # finished sentences should have their next token be a padding token
        if eos_token_id is not None:
            if pad_token_id is None:
                raise ValueError(
                    "If `eos_token_id` is defined, make sure that "
                    "`pad_token_id` is defined."
                )
            next_tokens = next_tokens * unfinished_sequences + pad_token_id * (
                        1 - unfinished_sequences)

        # Compute items to yield now, but wait until `unfinished_sequences` is
        # updated several lines below before yielding. Huggingface sets
        # corresponding unfinished_sequences val to 0 on the token AFTER
        # EOS_TOKEN, but we want it to be 0 starting WITH that token. Don't
        # compute earlier because we want to wait for next_tokens to be updated
        # first (sets finished sequence predictions to EOS) and don't do this
        # later in case any of the _top_word_probs inputs change (don't
        # think they do, but just being careful).
        next_toks, next_w2ps =_top_word_probs(probs, next_tokens,
                                              tokenizer, probs_per_token)

        # update generated ids, model inputs, and length for next step
        input_ids = torch.cat([input_ids, next_tokens[:, None]], dim=-1)
        model_kwargs = model._update_model_kwargs_for_generation(
            outputs, model_kwargs,
            is_encoder_decoder=model.config.is_encoder_decoder
        )

        # if eos_token was found in one sentence, set sentence to finished
        if eos_token_id is not None:
            unfinished_sequences = unfinished_sequences.mul(
                (next_tokens != eos_token_id).long())

        # Shape: (num_return_sequences, probs_per_word)
        yield next_toks, next_w2ps, unfinished_sequences.tolist()

        # Stop when each sentence is finished, or if we exceed the max length.
        if unfinished_sequences.max() == 0 or stopping_criteria(input_ids,
                                                                scores):
            if not synced_gpus:
                break
            else:
                this_peer_finished = True


@torch.no_grad()
def live_generate(
        model,
        tokenizer,
        inputs: Optional[torch.Tensor] = None,
        max_length: Optional[int] = None,
        min_length: Optional[int] = None,
        do_sample: Optional[bool] = None,
        temperature: Optional[float] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        typical_p: Optional[float] = None,
        repetition_penalty: Optional[float] = None,
        bad_words_ids: Optional[Iterable[int]] = None,
        bos_token_id: Optional[int] = None,
        pad_token_id: Optional[int] = None,
        eos_token_id: Optional[int] = None,
        no_repeat_ngram_size: Optional[int] = None,
        encoder_no_repeat_ngram_size: Optional[int] = None,
        num_return_sequences: Optional[int] = None,
        max_time: Optional[float] = None,
        max_new_tokens: Optional[int] = None,
        decoder_start_token_id: Optional[int] = None,
        use_cache: Optional[bool] = None,
        diversity_penalty: Optional[float] = None,
        logits_processor: Optional[LogitsProcessorList] = None,
        renormalize_logits: Optional[bool] = None,
        stopping_criteria: Optional[StoppingCriteriaList] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        output_scores: Optional[bool] = None,
        return_dict_in_generate: Optional[bool] = None,
        forced_bos_token_id: Optional[int] = None,
        forced_eos_token_id: Optional[int] = None,
        remove_invalid_values: Optional[bool] = None,
        synced_gpus: Optional[bool] = False,
        exponential_decay_length_penalty: Optional[Tuple[int, float]] = None,
        suppress_tokens: Optional[List[int]] = None,
        begin_suppress_tokens: Optional[List[int]] = None,
        forced_decoder_ids: Optional[List[List[int]]] = None,
        probs_per_token: Optional[int] = 5,
        **model_kwargs,
) -> Union[GenerateOutput, torch.LongTensor]:
    r"""
    Generates sequences of token ids for models with a language modeling head. The method supports the following
    generation methods for text-decoder, text-to-text, speech-to-text, and vision-to-text models:
        - *greedy decoding* by calling [`~generation_utils.GenerationMixin.greedy_search`]
            if `do_sample=False`.
        - *multinomial sampling* by calling [`~generation_utils.GenerationMixin.sample`]
            if `do_sample=True`.
    <Tip warning={true}>
    Apart from `inputs`, all the arguments below will default to the value of the attribute of the same name as
    defined in the model's config (`config.json`) which in turn defaults to the
    [`~modeling_utils.PretrainedConfig`] of the model.
    </Tip>
    Most of these parameters are explained in more detail in [this blog
    post](https://huggingface.co/blog/how-to-generate).
    Parameters:
        inputs (`torch.Tensor` of varying shape depending on the modality, *optional*):
            The sequence used as a prompt for the generation or as model inputs to the encoder. If `None` the
            method initializes it with `bos_token_id` and a batch size of 1. For decoder-only models `inputs`
            should of in the format of `input_ids`. For encoder-decoder models *inputs* can represent any of
            `input_ids`, `input_values`, `input_features`, or `pixel_values`.
        max_length (`int`, *optional*, defaults to `model.config.max_length`):
            The maximum length the generated tokens can have. Corresponds to the length of the input prompt +
            `max_new_tokens`. In general, prefer the use of `max_new_tokens`, which ignores the number of tokens in
            the prompt.
        max_new_tokens (`int`, *optional*):
            The maximum numbers of tokens to generate, ignoring the number of tokens in the prompt.
        min_length (`int`, *optional*, defaults to `model.config.min_length` or 10 if the config does not set any value):
            The minimum length of the sequence to be generated.
        do_sample (`bool`, *optional*, defaults to `model.config.do_sample` or `False` if the config does not set any value):
            Whether or not to use sampling ; use greedy decoding otherwise.
        temperature (`float`, *optional*, defaults to `model.config.temperature` or 1.0 if the config does not set any value):
            The value used to module the next token probabilities.
        penalty_alpha (`float`, *optional*, defaults to `model.config.penalty_alpha` or None if the config does not set any value):
            The values balance the model confidence and the degeneration penalty in contrastive search decoding.
        top_k (`int`, *optional*, defaults to `model.config.top_k` or 50 if the config does not set any value):
            The number of highest probability vocabulary tokens to keep for top-k-filtering.
        top_p (`float`, *optional*, defaults to `model.config.top_p` or 1.0 if the config does not set any value):
            If set to float < 1, only the smallest set of most probable tokens with probabilities that add up to
            `top_p` or higher are kept for generation.
        typical_p (`float`, *optional*, defaults to `model.config.typical_p` or 1.0 if the config does not set any value):
            The amount of probability mass from the original distribution to be considered in typical decoding. If
            set to 1.0 it takes no effect. See [this paper](https://arxiv.org/pdf/2202.00666.pdf) for more details.
        repetition_penalty (`float`, *optional*, defaults to `model.config.repetition_penalty` or 1.0 if the config does not set any value):
            The parameter for repetition penalty. 1.0 means no penalty. See [this
            paper](https://arxiv.org/pdf/1909.05858.pdf) for more details.
        pad_token_id (`int`, *optional*, defaults to `model.config.pad_token_id`):
            The id of the *padding* token.
        bos_token_id (`int`, *optional*, defaults to `model.config.bos_token_id`):
            The id of the *beginning-of-sequence* token.
        eos_token_id (`int`, *optional*, defaults to `model.config.eos_token_id`):
            The id of the *end-of-sequence* token.
        no_repeat_ngram_size (`int`, *optional*, defaults to `model.config.no_repeat_ngram_size` or 0 if the config does not set any value):
            If set to int > 0, all ngrams of that size can only occur once.
        encoder_no_repeat_ngram_size (`int`, *optional*, defaults to `model.config.encoder_no_repeat_ngram_size` or 0 if the config does not set any value):
            If set to int > 0, all ngrams of that size that occur in the `encoder_input_ids` cannot occur in the
            `decoder_input_ids`.
        bad_words_ids(`List[List[int]]`, *optional*, defaults to `model.config.bad_words_ids`):
            List of token ids that are not allowed to be generated. In order to get the token ids of the words that
            should not appear in the generated text, use `tokenizer(bad_words, add_prefix_space=True,
            add_special_tokens=False).input_ids`.
        num_return_sequences(`int`, *optional*, defaults to `model.config.num_return_sequences` or 1 if the config does not set any value):
            The number of independently computed returned sequences for each element in the batch.
        max_time(`float`, *optional*):
            The maximum amount of time you allow the computation to run for in seconds. generation will still
            finish the current pass after allocated time has been passed.
        attention_mask (`torch.LongTensor` of shape `(batch_size, sequence_length)`, *optional*):
            Mask to avoid performing attention on padding token indices. Mask values are in `[0, 1]`, 1 for tokens
            that are not masked, and 0 for masked tokens. If not provided, will default to a tensor the same shape
            as `input_ids` that masks the pad token. [What are attention masks?](../glossary#attention-mask)
        decoder_start_token_id (`int`, *optional*):
            If an encoder-decoder model starts decoding with a different token than *bos*, the id of that token.
        use_cache (`bool`, *optional*, defaults to `True`):
            Whether or not the model should use the past last key/values attentions (if applicable to the model) to
            speed up decoding.
        logits_processor (`LogitsProcessorList`, *optional*):
             Custom logits processors that complement the default logits processors built from arguments and a
             model's config. If a logit processor is passed that is already created with the arguments or a model's
             config an error is thrown. This feature is intended for advanced users.
        renormalize_logits (`bool`, *optional*, defaults to `False`):
            Whether to renormalize the logits after applying all the logits processors or warpers (including the
            custom ones). It's highly recommended to set this flag to `True` as the search algorithms suppose the
            score logits are normalized but some logit processors or warpers break the normalization.
        stopping_criteria (`StoppingCriteriaList`, *optional*):
             Custom stopping criteria that complement the default stopping criteria built from arguments and a
             model's config. If a stopping criteria is passed that is already created with the arguments or a
             model's config an error is thrown. This feature is intended for advanced users.
        output_attentions (`bool`, *optional*, defaults to `model.config.output_attentions` or `False` if the config does not set any value):
            Whether or not to return the attentions tensors of all attention layers. See `attentions` under
            returned tensors for more details.
        output_hidden_states (`bool`, *optional*, defaults to `model.config.output_hidden_states` or `False` if the config does not set any value):
            Whether or not to return the hidden states of all layers. See `hidden_states` under returned tensors
            for more details.
        output_scores (`bool`, *optional*, defaults to `model.config.output_scores` or `False` if the config does not set any value):
            Whether or not to return the prediction scores. See `scores` under returned tensors for more details.
        return_dict_in_generate (`bool`, *optional*, defaults to `model.config.return_dict_in_generate` or `False` if the config does not set any value):
            Whether or not to return a [`~utils.ModelOutput`] instead of a plain tuple.
        forced_bos_token_id (`int`, *optional*, defaults to `model.config.forced_bos_token_id`):
            The id of the token to force as the first generated token after the `decoder_start_token_id`. Useful
            for multilingual models like [mBART](../model_doc/mbart) where the first generated token needs to be
            the target language token.
        forced_eos_token_id (`int`, *optional*, defaults to `model.config.forced_eos_token_id`):
            The id of the token to force as the last generated token when `max_length` is reached.
        remove_invalid_values (`bool`, *optional*, defaults to `model.config.remove_invalid_values`):
            Whether to remove possible *nan* and *inf* outputs of the model to prevent the generation method to
            crash. Note that using `remove_invalid_values` can slow down generation.
        synced_gpus (`bool`, *optional*, defaults to `False`):
            Whether to continue running the while loop until max_length (needed for ZeRO stage 3)
        exponential_decay_length_penalty (`tuple(int, float)`, *optional*, defaults to `model.config.exponential_decay_length_penalty`):
            This Tuple adds an exponentially increasing length penalty, after a certain amount of tokens have been
            generated. The tuple shall consist of: `(start_index, decay_factor)` where `start_index` indicates
            where penalty starts and `decay_factor` represents the factor of exponential decay
        suppress_tokens  (`List[int]`, *optional*, defaults to `model.config.suppress_tokens`):
            A list of tokens that will be supressed at generation. The `SupressTokens` logit processor will set
            their log probs to `-inf` so that they are not sampled.
        begin_suppress_tokens  (`List[int]`, *optional*, defaults to `model.config.begin_suppress_tokens`):
            A list of tokens that will be supressed at the begining of the generation. The `SupressBeginTokens`
            logit processor will set their log probs to `-inf` so that they are not sampled.
        forced_decoder_ids (`List[List[int]]`, *optional*, defaults to `model.config.forced_decoder_ids`):
            A list of pairs of integers which indicates a mapping from generation indices to token indices that
            will be forced before sampling. For example, `[[1, 123]]` means the second generated token will always
            be a token of index 123.
        model_kwargs:
            Additional model specific kwargs will be forwarded to the `forward` function of the model. If the model
            is an encoder-decoder model, encoder specific kwargs should not be prefixed and decoder specific kwargs
            should be prefixed with *decoder_*.

    Yields
    ------
    tuple[list[str], list[dict], list[int]]: Each item has num_return_sequences
    items. First list contains predictions for next token(s). Second item
    contains word->prob dict for each next token (top k words + the sampled
    word). Third item shows which sequences are alive: 1 means we haven't hit
    EOS yet, 0 means we have.

    Examples:

    Multinomial Sampling:
    ```python
    >>> from transformers import AutoTokenizer, AutoModelForCausalLM
    >>> from transformers import AutoTokenizer, AutoModelForCausalLM
    >>> import torch
    >>> tokenizer = AutoTokenizer.from_pretrained("gpt2")
    >>> model = AutoModelForCausalLM.from_pretrained("gpt2")
    >>> prompt = "Today I believe we can finally"
    >>> input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    >>> for next_token, tok2prob in live_generate(
            model, tokenizer, input_ids, do_sample=True, max_length=30)
    >>> ):
    >>>     print(next_token)
    ```
    """
    unsupported = (
        'num_beams',
        'num_beam_groups',
        'prefix_allowed_tokens_fn',
    )
    for name in unsupported:
        if name in model_kwargs:
            raise ValueError(f'You passed in {name} but that '
                             'argument is not supported.')
    num_beams = 1
    num_beam_groups = 1
    prefix_allowed_tokens_fn = None

    if isinstance(inputs, (str, list)):
        inputs = tokenizer(inputs, return_tensors='pt').input_ids

    # 1. Set generation parameters if not already defined
    bos_token_id = (bos_token_id if bos_token_id is not None
                    else model.config.bos_token_id)

    do_sample = do_sample if do_sample is not None else model.config.do_sample
    num_return_sequences = (
        num_return_sequences if num_return_sequences is not None
        else model.config.num_return_sequences
    )
    logits_processor = (logits_processor if logits_processor is not None
                        else LogitsProcessorList())
    stopping_criteria = (stopping_criteria if stopping_criteria is not None
                         else StoppingCriteriaList())

    pad_token_id = (pad_token_id if pad_token_id is not None
                    else model.config.pad_token_id)
    eos_token_id = (eos_token_id if eos_token_id is not None
                    else model.config.eos_token_id)

    if eos_token_id is None and hasattr(model.config, "decoder"):
        eos_token_id = model.config.decoder.eos_token_id

    if pad_token_id is None and eos_token_id is not None:
        if model_kwargs.get("attention_mask", None) is None:
            logger.warning(
                "The attention mask and the pad token id were not set. "
                "As a consequence, you may observe "
                "unexpected behavior. Please pass your input's "
                "`attention_mask` to obtain reliable results."
            )
        logger.warning(
            f"Setting `pad_token_id` to `eos_token_id`:"
            f"{eos_token_id} for open-end generation."
        )
        pad_token_id = eos_token_id

    output_scores = (output_scores if output_scores is not None
                     else model.config.output_scores)
    output_attentions = (output_attentions if output_attentions is not None
                         else model.config.output_attentions)
    output_hidden_states = (
        output_hidden_states if output_hidden_states is not None
        else model.config.output_hidden_states
    )
    return_dict_in_generate = (
        return_dict_in_generate if return_dict_in_generate is not None
        else model.config.return_dict_in_generate
    )

    # 2. Define model inputs
    # inputs_tensor has to be defined
    # model_input_name is defined if model-specific keyword input is passed
    # otherwise model_input_name is None
    # all model-specific keyword inputs are removed from `model_kwargs`
    inputs_tensor, model_input_name, model_kwargs = model._prepare_model_inputs(
        inputs, bos_token_id, model_kwargs
    )
    batch_size = inputs_tensor.shape[0]

    # 3. Define other model kwargs
    model_kwargs["output_attentions"] = output_attentions
    model_kwargs["output_hidden_states"] = output_hidden_states
    model_kwargs["use_cache"] = use_cache

    accepts_attention_mask = "attention_mask" in set(
        inspect.signature(model.forward).parameters.keys())
    requires_attention_mask = "encoder_outputs" not in model_kwargs

    if (model_kwargs.get("attention_mask", None) is None
            and requires_attention_mask and accepts_attention_mask):
        model_kwargs[
            "attention_mask"] = model._prepare_attention_mask_for_generation(
            inputs_tensor, pad_token_id, eos_token_id
        )

    # decoder-only models should use left-padding for generation
    if not model.config.is_encoder_decoder:
        if pad_token_id is not None and torch.sum(
                inputs_tensor[:, -1] == pad_token_id) > 0:
            logger.warning(
                "A decoder-only architecture is being used, but right-padding "
                "was detected! For correct generation results, please set "
                "`padding_side='left'` when initializing the tokenizer."
            )

    if model.config.is_encoder_decoder and "encoder_outputs" not in model_kwargs:
        # if model is encoder decoder encoder_outputs are created
        # and added to `model_kwargs`
        model_kwargs = model._prepare_encoder_decoder_kwargs_for_generation(
            inputs_tensor, model_kwargs, model_input_name
        )

    # 4. Prepare `input_ids` which will be used for auto-regressive generation
    if model.config.is_encoder_decoder:
        input_ids = model._prepare_decoder_input_ids_for_generation(
            batch_size,
            decoder_start_token_id=decoder_start_token_id,
            bos_token_id=bos_token_id,
            model_kwargs=model_kwargs,
            device=inputs_tensor.device,
        )
    else:
        # if decoder-only then inputs_tensor has to be `input_ids`
        input_ids = inputs_tensor

    # 5. Prepare `max_length` depending on other stopping criteria.
    input_ids_seq_length = input_ids.shape[-1]
    if max_length is None and max_new_tokens is None:
        warnings.warn(
            "Neither `max_length` nor `max_new_tokens` has been set, "
            "`max_length` will default to " f"{model.config.max_length} "
            f"(`model.config.max_length`). Controlling `max_length` via the "
            "config is deprecated and `max_length` will be removed from "
            "the config in v5 of Transformers -- we recommend "
            "using `max_new_tokens` to control the maximum length "
            "of the generation.",
            UserWarning,
        )
    elif max_length is None and max_new_tokens is not None:
        max_length = max_new_tokens + input_ids_seq_length
    elif max_length is not None and max_new_tokens is not None:
        raise ValueError(
            "Both `max_new_tokens` and `max_length` have been set but they "
            "serve the same purpose -- setting a"
            " limit to the generated output length. Remove one of those "
            "arguments. Please refer to thedocumentation for more "
            " information. "
            "(https://huggingface.co/docs/transformers/main/en/main_classes/text_generation)"
        )
    # default to config if still None
    max_length = max_length if max_length is not None else model.config.max_length
    min_length = min_length if min_length is not None else model.config.min_length

    if min_length is not None and min_length > max_length:
        raise ValueError(
            f"Unfeasible length constraints: the minimum length "
            f"({min_length}) is larger than the maximum "
            f"length ({max_length})"
        )
    if input_ids_seq_length >= max_length:
        input_ids_string = ("decoder_input_ids" if
                            model.config.is_encoder_decoder else "input_ids")
        logger.warning(
            f"Input length of {input_ids_string} is {input_ids_seq_length}, "
            f"but `max_length` is set to"
            f" {max_length}. This can lead to unexpected behavior. "
            f"You should consider increasing `max_new_tokens`."
        )

    # 6. determine generation mode
    is_greedy_gen_mode = not do_sample
    if model.device.type != input_ids.device.type:
        warnings.warn(
            "You are calling .generate() with the `input_ids` being on a "
            "device type different"
            f" than your model's device. `input_ids` is on "
            f"{input_ids.device.type}, whereas the model"
            f" is on {model.device.type}. You may experience unexpected "
            f"behaviors or slower generation."
            " Please make sure that you have put `input_ids` to the"
            f" correct device by calling for example "
            f"input_ids = input_ids.to('{model.device.type}') before"
            " running `live_generate()`.",
            UserWarning,
        )

    # 7. prepare distribution pre_processing samplers
    logits_processor = model._get_logits_processor(
        repetition_penalty=repetition_penalty,
        no_repeat_ngram_size=no_repeat_ngram_size,
        encoder_no_repeat_ngram_size=encoder_no_repeat_ngram_size,
        input_ids_seq_length=input_ids_seq_length,
        encoder_input_ids=inputs_tensor,
        bad_words_ids=bad_words_ids,
        min_length=min_length,
        max_length=max_length,
        eos_token_id=eos_token_id,
        forced_bos_token_id=forced_bos_token_id,
        forced_eos_token_id=forced_eos_token_id,
        prefix_allowed_tokens_fn=prefix_allowed_tokens_fn,
        num_beams=num_beams,
        num_beam_groups=num_beam_groups,
        diversity_penalty=diversity_penalty,
        remove_invalid_values=remove_invalid_values,
        exponential_decay_length_penalty=exponential_decay_length_penalty,
        logits_processor=logits_processor,
        renormalize_logits=renormalize_logits,
    )

    # 8. prepare stopping criteria
    stopping_criteria = model._get_stopping_criteria(
        max_length=max_length, max_time=max_time,
        stopping_criteria=stopping_criteria
    )
    # 9. go into different generation modes
    if is_greedy_gen_mode:
        if num_return_sequences > 1:
            raise ValueError(
                f"num_return_sequences has to be 1, but is "
                f"{num_return_sequences} when doing greedy search."
            )

        # 10. run greedy search
        yield from live_greedy_search(
            model,
            tokenizer,
            input_ids,
            logits_processor=logits_processor,
            stopping_criteria=stopping_criteria,
            pad_token_id=pad_token_id,
            eos_token_id=eos_token_id,
            output_scores=output_scores,
            return_dict_in_generate=return_dict_in_generate,
            synced_gpus=synced_gpus,
            **model_kwargs,
        )

    else:
        # 10. prepare logits warper
        logits_warper = model._get_logits_warper(
            top_k=top_k,
            top_p=top_p,
            typical_p=typical_p,
            temperature=temperature,
            num_beams=num_beams,
            renormalize_logits=renormalize_logits,
        )

        # 11. expand input_ids with `num_return_sequences` additional
        # sequences per batch
        input_ids, model_kwargs = model._expand_inputs_for_generation(
            input_ids=input_ids,
            expand_size=num_return_sequences,
            is_encoder_decoder=model.config.is_encoder_decoder,
            **model_kwargs,
        )

        # 12. run sample
        yield from live_sample(
            model,
            tokenizer,
            input_ids,
            logits_processor=logits_processor,
            logits_warper=logits_warper,
            stopping_criteria=stopping_criteria,
            pad_token_id=pad_token_id,
            eos_token_id=eos_token_id,
            output_scores=output_scores,
            return_dict_in_generate=return_dict_in_generate,
            synced_gpus=synced_gpus,
            **model_kwargs,
        )


def truncate_if_necessary(tokenizer, text, max_new_tokens,
                          do_strip=True):
    """Truncate text prompt so that the requested generation length can
    execute without error (this is limited by model_max_length).

    Parameters
    ----------
    tokenizer
    text: str
    max_new_tokens: int
    do_strip: bool

    Returns
    -------
    dict
    """
    if do_strip:
        text = text.rstrip()
    xb = tokenizer(text, return_tensors='pt')
    ids = xb.input_ids.squeeze(0)
    original_len = len(ids)
    original_len_words = len(text.split())
    ids = ids[-tokenizer.model_max_length + max_new_tokens:].squeeze(0)
    text = tokenizer.decode(ids)
    new_len = len(ids)
    new_len_words = len(text.split())
    res = {
        'text': text,
        # Add batch dimension back in so we can more easily pass it to
        # live_generate.
        'input_ids': ids.unsqueeze(0),
        'original_length': original_len,
        'original_length_words': original_len_words,
        'truncated_length': new_len,
        'truncated_length_words': new_len_words,
    }
    return res