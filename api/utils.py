from typing import Any, Callable, Optional, TypeVar
from functools import wraps
import inspect
import os
import time
import logging
import re
import string
from typing import *
from fedrit.settings import (
    VALID_CHARS, VALID_NAME_LEN_MAX, VALID_NAME_CHARS, logger
)
from secrets import token_urlsafe

lflogger = logging.getLogger('logf')
logger = logging.getLogger(__name__)
    

class SLIT:
    """ used for typehints """
    platformuser = 'api.models.PlatformUser'
    platform = 'api.models.Platform'
    post = 'api.models.Post'
    comment = 'api.models.Comment'
    usertoken = 'api.models.UserToken'
    token = 'api.models.Token'


T = TypeVar("T", bound=Callable[..., Any])

def logf(level: Optional[int] = logging.DEBUG) -> Callable[[T], T]:
    """
    A decorator that logs the execution time, function name, arguments, keyword arguments,
    and return value of a function using a specified log level.

    Args:
        level (int, optional): The log level to use for logging. Defaults to logging.DEBUG.

    Returns:
        Callable[[T], T]: The wrapped function.
    """
    def decorator(func: T) -> T:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Start the timer and execute the function.
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()

            frame = inspect.getframeinfo(inspect.currentframe().f_back)
            lineno = frame.lineno

            # Calculate the execution time and format the log message.
            extime = end_time - start_time
            funcfname = os.path.basename(
                inspect.getmodule(func).__file__)

            message = (f"{funcfname}:{lineno} {extime:.4f} {func.__name__}() "
                       f"| args={args} kwargs={kwargs}) >>>>> {result}")

            # Log the message using the specified level.
            lflogger.log(level, message)

            return result
        return wrapper
    return decorator


@logf(level='info')
def pal(*args) -> str:
    """enables log funcs to be used like print()

    Returns:
        str: str that was used in log msg
    """
    msg = ' '.join((str(a) for a in args))
    print('PRINT PAL():', msg)
    logger.debug(f'PAL() LOGGER: {msg}')
    
    return msg


@logf()
def valid_uuid(string):
    regex = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12}$')
    return bool(regex.match(string))

@logf()
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

@logf()
def valid_username(username: str) -> bool:
    """Determines if a username is valid.

    Args:
        username (str): username to determine validity of

    Returns:
        bool: True if valid, False if invalid
    """
    reg = r'^[a-zA-Z0-9-_]{1,}?@[a-zA-Z0-9-_]{1,}$'
    print(re.search(reg, username))
    if re.search(reg, username):
        return True
    return False

@logf()
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

@logf()
def gen_token_str() -> str:
    return f'fdr-{token_urlsafe(32)}'

@logf()
def valid_token_str(tokenstr: str) -> bool:
    """_summary_

    Args:
        tokenstr (str): _description_

    Returns:
        bool: _description_
    """
    rmatch = re.match(r'^(fdr-[a-zA-Z_\-0-9]+)', str(tokenstr))
    
    if rmatch is None:
        return False
    
    rgroups = rmatch.groups()
    if len(rgroups) == 1 and rgroups[0] == tokenstr:
        return True
    return False



@logf()
def def_kwargs(*args, **kwargs) -> dict:
    dk = dict(kwargs)
    dk['id'] = {'required': False}
    dk['created_at'] = {'read_only': True},
    dk['updated_at'] = {'read_only': True}
    print('dk', dk)
    return dk

@logf()
def modchoice(t: str, choice: tuple):
    t = str(t).upper()
    for c in choice:
        if c[0] == t:
            return c[1]




