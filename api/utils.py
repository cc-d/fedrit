import string
from typing import *

VALID_CHARS = string.ascii_letters + string.digits + '_' + '-'

def valid_str(vstr: str, str_type: str) -> bool:
    """ is this string a valid username/community name """
    str_type = str(str_type).lower()
    str_type_table = {
        'username': {
            'maxlen': 30,
            'chars': VALID_CHARS,
        },
        'communityname': {
            'maxlen': 30,
            'chars': VALID_CHARS,
        },
        'platformname': {
            'maxlen': 30,
            'chars': VALID_CHARS
        }
    }

    if str_type not in str_type_table:
        str_type = 'username'

    if len(vstr) > 0 and len(vstr) <= str_type_table[str_type]:
        unique_chars = ''.join(list(set(vstr)))
        for uc in unique_chars:
            if uc not in VALID_CHARS:
                return False
        return True
    return False