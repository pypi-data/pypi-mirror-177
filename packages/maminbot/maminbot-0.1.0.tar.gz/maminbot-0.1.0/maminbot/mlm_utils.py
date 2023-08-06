"""Functionality to help us work with masked language models.
"""

from collections import Mapping
from itertools import product
import numpy as np
import torch
import torch.nn.functional as F
from tqdm.auto import tqdm
import warnings

from htools import eprint, timer, block_timer, bound_args, params, identity, \
    Trie, deprecated


def fill_multi_mask_auto(text, pipe, top_k=5, **kwargs):
    """Fill multiple masked tokens in an input string in an independent manner
    using the builtin Huggingface pipeline functionality. This is just a
    wrapper to reshape outputs a bit to be consistent with the interface our
    other mask filling functions follow.

    Parameters
    ----------
    text: str
        Input text that already has multiple words masked. Careful: not all
        models use the same mask token, so make sure you're using the right
        one for your pipeline.
    pipe: transformers.FillMaskPipeline
        E.g. pipe = pipeline('fill-mask', model='bert-base-cased')
    top_k: int
    kwargs: any
        Ignored. Just here to maintain a consistent interface for multi mask
        functions.

    Returns
    -------
    dict:
    'token_probs'
        a list of dicts where the i'th item in the list corresponds to the
        i'th masked token. Each dict maps the top_k predicted token strings to
        probabilities.
    'seq2probs'
        a dict mapping tuples of predicted tokens (each with length m, where m
        is the number of masked tokens in the input) to a list of m
        probabilities.
    'seq2prob'
        a dict like seq2probs, but values are the product of each token's
        predicted probabilities. We also sort this dict so the most likely
        seqs come first.
    """
    res = pipe(text, top_k=top_k)
    if isinstance(res[0], Mapping):
        res = [res]
    token_probs = [{d['token_str']: d['score'] for d in row}
                   for row in res]
    seq2probs = {row: [token_probs[i][tok] for i, tok in enumerate(row)]
                 for row in product(*token_probs)}
    return {
        'token_probs': token_probs,
        'seq2probs': seq2probs,
        'seq2prob': dict(sorted(
            [(k, np.product(v)) for k, v in seq2probs.items()],
            key=lambda x: x[1], reverse=True
        ))
    }


@deprecated(msg='Soft deprecation: fill_multi_mask_left_to_right hasn\'t been '
            'tested on mask-filling pipelines like "roberta-base", and may '
            'not work as expected due to their special space characters. We '
            'suggest using fill_multi_mask_auto or '
            'fill_multi_mask_exhaustive.')
def fill_multi_mask_left_to_right(text, pipe, top_k=5, **kwargs):
    """Fill multiple masked tokens in an input string in a dependent manner.
    Huggingface pipeline can fill multiple tokens in a single pipeline call
    but (depending on the model) this will often make those predictions
    independently.

    Fill 1 masked token at a time, starting with the left-most masked token and
    working rightwards. At each iteration, we predict on a string where the
    *previous* masked token is filled with the most likely prediction from
    the previous step. This makes the token predictions dependent rather
    than independent (hopefully leading to more context-aware completions).
    It is greedy, however - we only keep the 1 most likely token at each step.

    We make a total of m forward passes where m is the total number of
    masked tokens, and we end up with k potential sequences
    where k is the number of top tokens we keep per forward pass. (This number
    will often be *much* lower than our exhaustive mask filling strategy
    because we only keep the top 1 prediction at each unmasking step.
    We do still return a total of k*m different tokens with probabilities,
    but only k of those combinations form valid predictions.)

    Parameters
    ----------
    text: str
        Input text that already has multiple words masked. Careful: not all
        models use the same mask token, so make sure you're using the right
        one for your pipeline.
    pipe: transformers.FillMaskPipeline
        E.g. pipe = pipeline('fill-mask', model='bert-base-cased')
    top_k: int
    kwargs: any
        Ignored. Just here to maintain a consistent interface for multi mask
        functions.

    Returns
    -------
    dict:
    'token_probs'
        a list of dicts where the i'th item in the list corresponds to the
        i'th masked token. Each dict maps the top_k predicted token strings to
        probabilities.
    'seq2probs'
        a dict mapping tuples of predicted tokens (each with length m, where m
        is the number of masked tokens in the input) to a list of m
        probabilities.
    'seq2prob'
        a dict like seq2probs, but values are the product of each token's
        predicted probabilities. We also sort this dict so the most likely
        seqs come first.
    """
    xb = pipe.tokenizer(text, return_tensors='pt')
    mask_idx = pipe.get_masked_index(xb.input_ids)[:, -1].tolist()
    prev_pred = pipe.tokenizer.mask_token_id
    all_res = []
    n_mask = len(mask_idx)
    running_top_toks = []
    running_top_probs = []
    for i, prev_i in tqdm(zip(mask_idx, [None] + mask_idx),
                          total=n_mask, desc='unmask'):
        if prev_i is not None:
            xb['input_ids'][0, prev_i] = prev_pred
        with torch.no_grad():
            res = pipe.model(xb.input_ids)
        probs = F.softmax(res.logits[0, i], dim=-1)
        top_probas, top_idx = torch.topk(probs, top_k, dim=-1)
        pred_tokens = pipe.tokenizer.convert_ids_to_tokens(top_idx)
        running_top_toks.append(pred_tokens[0])
        running_top_probs.append(top_probas[0].item())
        res = dict(zip(pred_tokens, top_probas.tolist()))
        prev_pred = top_idx[0]
        all_res.append(res)

    running_top_toks.pop(-1)
    running_top_probs.pop(-1)
    total_prob = np.product(running_top_probs)
    seq2probs = {}
    seq2prob = {}
    for k, v in all_res[-1].items():
        key = tuple(running_top_toks + [k])
        seq2probs[key] = running_top_probs + [v]
        seq2prob[key] = total_prob * v
    return {
        'token_probs': all_res,
        'seq2probs': seq2probs,
        'seq2prob': seq2prob
    }


def fill_multi_mask_exhaustive(text, pipe, top_k=5, space_char=' '):
    """Given a piece of text with multiple masked tokens, unmask them from left
    to right, exploring all possible branches of the tree of top predictions.
    We need to make k^(i-1) forward passes at each step (where k is the number
    of top predicted tokens we keep from each forward pass, and i is the
    1-indexed number marking which masked token we're filling), each operating
    on a different input string. We end up with k^i possible sequences and
    \sum^{m}_{i=1} m * k^{(i - 1)}
    total forward passes.

    Parameters
    ----------
    text: str
        Input text that already has multiple words masked. Careful: not all
        models use the same mask token, so make sure you're using the right
        one for your pipeline.
    pipe: transformers.FillMaskPipeline
        E.g. pipe = pipeline('fill-mask', model='bert-base-cased')
    top_k: int
    space_char: str
        Character tokenizer uses to represent space. For bert etc. this should
        be a string containing a single space. For roberta etc this should
        be 'Ġ'.

    Returns
    -------
    dict:
    'token_probs'
        a list of lists of dicts, where the i'th nested list maps to the
        i'th masked token. Dict j within a nested list maps token strings to
        predicted probabilities for the j'th pipeline call for that mask index.
        E.g. res['token_probs'][2][0] contains token probs for the 3rd masked
        token, if we filled the 0th and 1st mask spots with their single most
        likely predictions. NOTE: this is different than the token_probs
        returned by the other multi-mask filling functions. Use the
        all_step_seq2probs function to get something equivalent.
    'seq2probs'
        a dict mapping tuples of predicted tokens (each with length m, where m
        is the number of masked tokens in the input) to a list of m
        probabilities.
    'seq2prob'
        a dict like seq2probs, but values are the product of each token's
        predicted probabilities. We also sort this dict so the most likely
        seqs come first.
    'trie'
        maps to a Trie where each node is a predicted token (and which has an
        associated 'prob' attribute).
    """
    if not space_char.strip() and 'Ġ' in pipe.tokenizer.vocab:
        warnings.warn('Are you sure you passed the correct space_char for '
                      'fill_multi_mask_exhaustive? Looks like it should '
                      f'probably be "Ġ", not {space_char!r}.')
    text = [text]
    mask_token = pipe.tokenizer.mask_token
    xb = pipe.tokenizer(text, return_tensors='pt')
    seq_len = xb.input_ids.shape[-1]
    mask_idx = pipe.get_masked_index(xb.input_ids)[:, -1].tolist()
    all_res = []
    # Seqs is a list of lists where each nested list represents 1 predicted
    # seq and contains n_mask tuples of (tok, prob). We use it to construct
    # our trie.
    seqs = []
    n_mask = len(mask_idx)
    for i, prev_i in tqdm(zip(mask_idx, [None] + mask_idx),
                          total=n_mask, desc='Unmask'):
        with torch.no_grad():
            res = pipe.model(xb.input_ids)
        assert res.logits.shape[1] == seq_len, \
            f'Sequence length should remain {seq_len} but for mask_idx {i}, '\
            f'found seq len {res.logits.shape[1]}.'
        probs = F.softmax(res.logits[:, i, :], dim=-1)
        top_probas, top_idx = torch.topk(probs, top_k, dim=-1)
        pred_tokens = [pipe.tokenizer.convert_ids_to_tokens(row)
                       for row in top_idx]
        res = [dict(zip([pred.replace(space_char, ' ', 1) for pred in preds],
                        probas.tolist()))
               for preds, probas in zip(pred_tokens, top_probas)]
        all_res.append(res)
        if not seqs:
            # We only call this on first iteration, so we know
            # pred_tokens only has 1 row.
            seqs = [[(k, v)] for k, v in res[0].items()]
        else:
            seqs = [[*existing_seq, (k, v)]
                    for existing_seq, row in zip(seqs, res)
                    for k, v in row.items()]

        # Update token ids in batch. Originally tried to update text itself
        # and re-tokenized on each iteration but that turned out to be a bit
        # buggy: different tokenizers handle spaces differently, also have to
        # account for subwords with leading "##" (in both cases, input
        # text and output text are not formatted in the same way).
        new_input_ids = []
        for row, idx_row in zip(xb.input_ids, top_idx):
            row = row.repeat(top_k, 1)
            row[:, i] = idx_row
            new_input_ids.append(row)
        xb['input_ids'] = torch.cat(new_input_ids)
        xb['attention_mask'] = xb.attention_mask.repeat(top_k, 1)

    # Trie will help us work with sequences and probabilities later.
    T = Trie()
    for row in seqs:
        toks, probs = map(list, zip(*row))
        T.append(toks)
        for i in range(1, n_mask + 1):
            # Setting attributes this way is not ideal but in this case we
            # know
            # a. every seq we're looking for has already been added to trie
            # b. nodes are not shared between sequences with different common
            # prefixes. E.g. the leaf node in ['a', 'b', 'c'] is different
            # than the leaf node in ['x', 'y', 'c'] so settings node-level
            # attributes should be ok.
            node = T._find(toks[:i])
            node.prob = probs[i - 1]

    seq2probs = {}
    seq2prob = {}
    for seq in T:
        all_probs, total_prob = _seq2probs_from_trie(seq, T)
        key = tuple(seq)
        seq2probs[key] = all_probs
        seq2prob[key] = total_prob
    seq2prob = dict(sorted(seq2prob.items(),
                           key=lambda x: x[1], reverse=True))
    return {
        'token_probs': all_res,
        'seq2probs': seq2probs,
        'seq2prob': seq2prob,
        'trie': T
    }


def _seq2probs_from_trie(seq, T):
    """Used by fill_multi_mask_exhaustive to get the sequence of probabilities
    (and overall probability) for each sequence of predicted tokens. This is
    only used after the trie has been fully constructed.

    Parameters
    ----------
    seq: list[str]
        List of predicted tokens, where index corresponds to mask index (e.g.
        the first string should fill the first masked span).
    T: htools.Trie[list[str]]

    Returns
    -------
    tuple[list[float], float]: First item is a list of predicted probabilities
    for each token in seq at the corresponding index. Second item is the
    product of those probabilities, essentially the overall probability of this
    sequence.
    """
    # We know all sequences are the same length in this use case.
    expected_length = len(next(iter(T)))
    length = len(seq)
    if length != expected_length:
        raise ValueError(f'Invalid sequence length {length}. '
                         f'Expected {expected_length}.')
    # Use list rather than dict because we can predict the same word
    # for multiple timesteps, which results in duplicate keys in dict
    # (meaning 1 prob would be discarded).
    nodes = [getattr(T._find(seq[:i]), 'prob', 0)
             for i in range(1, length + 1)]
    return nodes, np.prod(nodes)


def next_step_seq2probs(partial_seq, res):
    """For a given (possible partial) sequence of predicted token strings,
    what are the predicted probabilities for the next step? This is mostly
    necessary because our exhaustive mask filling function output is a little
    wonky - with the auto and left to right versions, we just return the
    dict at the next index in our res['token_probs'] list.

    Parameters
    ----------
    partial_seq: list[str]
        Contains 0 or more tokens.
    res: dict
        Result of one of our multi mask filling functions.

    Returns
    -------
    dict[str, float]: Maps tokens that are likely to occur next to their
    predicted probabilities.
    """
    if 'trie' in res:
        if not partial_seq:
            node = res['trie'].head
        else:
            node = res['trie']._find(partial_seq)
        return {k: v.prob for k, v in node.edges.items()}
    return res['token_probs'][len(partial_seq)]


def all_step_seq2probs(seq, res):
    """Get a list of tok2prob dicts, 1 for each mask index when we filled a
    string with multiple masked tokens. For our auto and left to right
    functions, this literlaly just returns our token_probs list. Our exhaustive
    function output is a bit wonky so we have to do some surgery to get an
    equivalent data structure there.

    Parameters
    ----------
    seq: list[str]
        Contains m tokens, where m is the number of masked tokens in the
        corresponding input string.
    res: dict
        Result of one of our multi mask filling functions.

    Returns
    -------
    list[dict[str, float]]: Maps tokens that are likely to occur next to their
    predicted probabilities. Contains one dict for each masked token in the
    corresponding input.
    If seq was not one of our predicted seqs, we return an empty list.
    """
    if 'trie' in res:
        # Tricky bug if we don't check for seq presence: our first next_step
        # call uses an empty sequence to get the first dict of predictions, but
        # that also means we were returning probabilities for sequences that
        # didn't exist. Better to just be extra safe, and the trie makes it
        # pretty fast.
        if seq not in res['trie']:
            return []
        return [next_step_seq2probs(seq[:i], res) for i in range(len(seq))]
    return res['token_probs']