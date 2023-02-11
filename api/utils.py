import re
import string
from typing import *
from .models import (
    Platform, PlatformUser, Community, Post,
)
from fedrit.settings import VALID_CHARS, VALID_NAME_LEN_MAX, VALID_NAME_CHARS


def valid_uuid(string):
    regex = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12}$')
    return bool(regex.match(string))


def valid_name(vstr: str, add_chars: str = '') -> bool:
    """Determines if a name str is valid for a provided str type, using
    str length and a character subset.

    Args:
        vstr (str): string to validate
        add_chars (str): any characters in this string will be added
            to the valid character set.

    Returns:
        bool: is this str valid for this type
    """
    valid_chars = VALID_NAME_CHARS + add_chars

    if len(vstr) > 0 and len(vstr) <= VALID_NAME_LEN_MAX:
        unique_chars = ''.join(list(set(vstr)))
        for uc in unique_chars:
            if uc not in VALID_CHARS:
                return False
        return True
    return False


def valid_username(username: str) -> bool:
    """Determines if a username is valid.

    Args:
        username (str): username to determine validity of

    Returns:
        bool: True if valid, False if invalid
    """
    reg = r'^[a-zA-Z0-9-_]{1,}?@?[a-zA-Z0-9-_]{1,}$'
    return re.search(reg, username)


def valid_url(url: str) -> bool:
    """Determines if a string is a valid URL

    Args:
        url (str): provided url str

    Returns:
        bool: if str is valid url
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        # domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None


def def_kwargs(*args, **kwargs) -> dict:
    dk = dict(kwargs)
    dk['id'] = {'required': False}
    dk['created_at'] = {'read_only': True},
    dk['updated_at'] = {'read_only': True}
    print('dk', dk)
    return dk

def modchoice(t: str, choice: tuple):
    t = str(t).upper()
    for c in choice:
        if c[0] == t:
            return c[1]

