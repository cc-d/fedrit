from secrets import token_urlsafe
from models import PlatformUser, Platform, UserToken
from typing import *
from utils import gen_token_str


def gen_user_token(
    user: Optional[PlatformUser] = None, 
    platform: Optional[Platform] = None
) -> UserToken:
    """_summary_

    Args:
        user (Optional[PlatformUser], optional): _description_. Defaults to None.
        platform (Optional[Platform], optional): _description_. Defaults to None.

    Returns:
        UserToken: _description_
    """
    return UserToken.objects.create(user=user, platform=platform)
