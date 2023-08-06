"""Utilities for interacting with our cloud db (Deta Base - not a typo).
"""
import pandas as pd
from deta import Deta
import warnings

from htools import tolist


def fetch_records(user='', tags=(), tag_strategy='any', prompt_contains='',
                  text_contains='', db=None):
    """Fetch records from Deta Base maminbotDB.

    Parameters
    ----------
    user: str
        Optionally provide one of the names in maminbot.config.users to only
        retrieve text from that user.
    tags: list[str]
        Optionally provide one or more tags to look for. Depending on tag
        strategy, you can choose to keep only rows that contain all tags or
        keep rows that contain any of the specified tags.
    tag_strategy: str
        "any" or "all". "any" returns rows that contain any of the tags the
        user passed in, while "all" requires rows to possess all specified tags
        in order to be returend.
    prompt_contains: str
        If provided, we only return rows where the "text" columnn contains the
        specified text. Case insensitive.
    text_contains: str
        If provided, we only return rows where the "prompt" columnn contains
        the specified text. Case insensitive. Rows with no prompt will never be
        returned.
    db: deta.base._Base
        Deta Base object. Typically created by
        `deta.Deta(project_key).Base(project_name)` where project_name is
        "maminbotDB".

    Returns
    -------
    pd.DataFrame
    """
    if not db:
        db = connect_db()
    query = {}
    if user:
        query['user'] = user
    tags = tolist(tags)
    if tags and tag_strategy not in ('any', 'all'):
        raise ValueError(f'Got unexpected tag_strategy {tag_strategy}. '
                         f'Should be "any" or "all".')
    res = db.fetch(query).items
    df = pd.DataFrame(res)
    if tags:
        func = getattr(__builtins__, tag_strategy)
        df = df[df.tags.apply(lambda x: func(tag in x for tag in tags))]
    if prompt_contains:
        df = df[df.prompt.str.lower().str.contains(prompt_contains.lower())]
    if text_contains:
        df = df[df.text.str.lower().str.contains(text_contains.lower())]
    df['dt'] = pd.to_datetime(df.dt)
    return df.reset_index(drop=True)


def load_creds():
    """
    Output isn't actually mutated but streamlit always raises a warning here
    unless we allow output mutation.
    NOTE: debug must be after st.cache. Do NOT use htools.decorate_functions
    because then debug will be on the outside and caching won't work.
    """
    df = pd.read_csv('data/creds/deta.csv')
    return df.to_dict(orient='records')[0]


def connect_db(key='', name=''):
    """Load deta.Base object that can be used to fetch items from our cloud
    database.

    Parameters
    ----------
    key: str
        "project_key". Should not expose this on github.
    name: str
        "project_name". This doesn't need to be private.

    Returns
    -------
    deta.base._Base
    """
    if not (key and name):
        warnings.warn(f'Missing key and/or name so defaulting to '
                      f'{DETA_CREDS["project_name"]} project creds.')
        key = DETA_CREDS['project_key']
        name = DETA_CREDS['project_name']
    for obj in (key, name):
        if not isinstance(obj, str) or obj[0] == '{':
            raise ValueError(
                'Input args should be strings. It looks like you might have '
                f'passed in a dict or stringified dict by accident: {obj}'
            )
    deta = Deta(key)
    return deta.Base(name)


DETA_CREDS = load_creds()
