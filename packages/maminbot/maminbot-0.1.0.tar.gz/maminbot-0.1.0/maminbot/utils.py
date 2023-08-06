from pathlib import Path
import sys


def load_hf_api_key(paths=('~/.huggingface', '~/secrets/.huggingface')):
    """
    Parameters
    ----------
    paths: Iterable[str]
        The paths to check for huggingface api keys. Order matters: we return
        the contents of the first non-empty file in the list.

    Returns
    -------
    str: Huggingface api key. Guaranteed to be truthy if we hit the return
    statement. Raises a FileNotFoundError if NONE of the paths exist/contain
    truthy strings.
    """
    for path in paths:
        try:
            with open(Path(path).expanduser(), 'r') as f:
                key = f.read().strip()
        except FileNotFoundError:
            key = ''
        if key: return key
    raise FileNotFoundError('Could not find any huggingface api key. '
                            f'Checked paths: {paths}')


def update_cli_command(**kwargs):
    """Used in s01 to add default args to our language model training script.
    This is helpful because adding defaults in dataclass subclasses is
    surprisingly difficult.

    Parameters
    ----------
    kwargs: any

    """
    for k, v in kwargs.items():
        if f'--{k}' not in sys.argv:
            sys.argv.extend([f'--{k}', str(v)])