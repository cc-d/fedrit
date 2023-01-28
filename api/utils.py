import re
import string
from typing import *
from .models import (
    Platform, PlatformUser, Community, CommunityPost,
)

VALID_CHARS = string.ascii_letters + string.digits + '_' + '-'


def valid_name(vstr: str, str_type: str) -> bool:
    """Determines if a name str is valid for a provided str type, using
    str length and a character subset.

    Args:
        vstr (str): string to validate
        str_type (str): type of string being validated

    Returns:
        bool: is this str valid for this type
    """
    str_type = str(str_type).lower()
    str_type_table = {
        'username': {
            'maxlen': PlatformUser.origin_username.max_length,
            'chars': VALID_CHARS,
        },
        'communityname': {
            'maxlen': Community.name.max_length,
            'chars': VALID_CHARS,
        },
        'platformname': {
            'maxlen': Platform.name.max_length,
            'chars': VALID_CHARS
        }
    }

    if str_type not in str_type_table:
        str_type = 'username'

    if len(vstr) > 0 and \
        len(vstr) <= str_type_table[str_type]['maxlen']:
        unique_chars = ''.join(list(set(vstr)))
        for uc in unique_chars:
            if uc not in VALID_CHARS:
                return False
        return True
    return False


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