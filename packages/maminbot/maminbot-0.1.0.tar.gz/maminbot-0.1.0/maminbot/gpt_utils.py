import numpy as np
from htools import load


def sample_prompt_examples(task, n=3, to_str=True):
    """Helper to dynamically construct prompts which include a numbered list.
    I think varying the examples a bit should help us get more variety in the
    completions.

    Parameters
    ----------
    task: str
        Corresponds to a file like ./data/dynamic_prompt_data/{task}.txt.
        The file should contain 1 prompt per line, each with a leading hyphen.
        There should typically also be a corresponding prompt like
        ~/jabberwocky/data/prompts/{task}.yaml.
    n: int
        Number of examples to sample. This should be less than the number your
        prompt requests: e.g. if you want 3 examples and 3 completions, your
        prompt would specify that the list contains 6 items (3 + 3) and you
        would pass n = 3 into this function.

    Returns
    -------
    str or list[str]: Depends on value of to_str arg. If True, we return a
    single str where each line is prefixed by a number and a trailing number
    is added at the end. (See below.) If False, we return a list of strings
    without adding any row numbers.

    # Example response when to_str=True (newlines have been inserted here to
    comply with pep8 conventions):
    >>> print(sample_prompt_examples('creative_writing_ideas'))

    1. Imagine that a trolley is heading towards a person tied to the tracks.
    You can pull the lever to divert it to another track, saving the person,
    but then your life savings will be destroyed. What do you do?
    2. Write a story in which a character tries to reconnect with a former
    love from a different era.
    3. You have been invited to a gala at a grand estate. Describe what you
    wear and what happens during the evening.
    4.
    """
    text = load(f'data/dynamic_prompt_data/{task}.txt')
    rows = [row.strip('-') for row in text.splitlines() if row.strip('-')]
    sampled = list(np.random.choice(rows, n, replace=False))
    if to_str:
        sampled = [f'{i}. {row}' for i, row in enumerate(sampled, 1)]
        return '\n'.join(sampled) + f'\n{n + 1}.'
    return sampled
