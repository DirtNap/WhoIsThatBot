"""Utility features for the reddit bot."""
from typing import Callable, List, Optional, Tuple

import praw
import spacy

from django.conf import settings

from . import models as rb_models

class Error(Exception):
    """Base error for this module."""
    pass

class ArgumentError(Error, ValueError):
    """Raised on invalid argument values."""
    pass

NLP_PARSER = spacy.load(settings.SPACY_MODEL_BASE)

def get_reddit_client(client_id:Optional[str]=None, client_secret:Optional[str]=None,
                      user_agent:Optional[str]=None,
                      client_username:Optional[str]=None, client_password:Optional[str]=None) -> praw.Reddit:
    """Get a reddit client based on provided or default configuration."""
    kwargs = {
        'client_id': client_id or settings.PRAW_CLIENT_ID,
        'client_secret': client_secret or settings.PRAW_CLIENT_SECRET,
        'user_agent': user_agent or f'WhoIsThat Bot/{settings.APPLICATION_VERSION}',
    }
    if not client_username:
        client_username = settings.PRAW_CLIENT_USERNAME
    if not client_password:
        client_password = settings.PRAW_CLIENT_PASSWORD
    if any((client_username, client_password)):
        if not all((client_username, client_password)):
            raise ArgumentError('Incompatible client_username and client_password for reddit client.')
        kwargs['client_username'] = client_username
        kwargs['client_password'] = client_password
    return praw.Reddit(**kwargs)


def get_tokens(parser:Callable, text:str) -> Tuple[List[str], List[Tuple[str, str]]]:
    """Parses texts and returns lists of persons and other found entities."""
    parsed = parser(text)
    people = []
    others = []
    for entity in parsed.ents:
        if entity.label_ == 'PERSON':
            people.append(entity.text)
        else:
            others.append((entity.text, entity.label_))
    return people, others
