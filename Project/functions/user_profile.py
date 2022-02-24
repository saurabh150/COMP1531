"""
This module sets majority of attributes in a user's profile. These include
name, email, handle.
A function also exists to retrieve user profile details.
"""
# This disables the error for overwriting ValueError for our error handler.
# pylint: disable=W0622

# GET
# user/profile
# (token, u_id)
# { email, name_first, name_last, handle_str }

# ValueError when:
# User with u_id is not a valid user

# For a valid user, returns information about their
# email, first name, last name, and handle

from .data import get_users, is_used_handle, get_user, find_channel_with_channel_id
from .helper import is_invalid_name, is_used_email, is_invalid_email
from .helper import verify_token, is_valid_handle, u_id_exists
from .exceptions import ValueError

def user_profile(token, u_id):
    """Given an active token return an authorised user's profile details"""
    if not u_id_exists(u_id):
        raise ValueError("U_id is not a valid user")
    verify_token(token)
    user = get_user(u_id)
    return {
        'email' : user['email'],
        'name_first' : user['name_first'],
        'name_last' : user['name_last'],
        'handle_str' : user['handle_str'],
        'profile_img_url': user['profile_img_url']
    }

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# PUT
# user/profile/setemail
# (token, email)
# {}

# ValueError when:
# Email entered is not a valid email using the method provided here
# (unless you feel you have a better method).
# Email address is already being used by another user

def user_profile_setemail(token, email):
    """Given an active token, sets email and returns empty dict"""
    verify_token(token)

    if is_invalid_email(email):
        raise ValueError("Invalid email entered")
    if is_used_email(email):
        raise ValueError("Email has been used before")

    users = get_users()
    for user in users:
        if user['token'] == token:
            user['email'] = email

    return {}

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*

# PUT
# user/profile/setname
# (token, name_first, name_last)
# {}

# ValueError when:
# name_first is not between 1 and 50 characters in length
# name_last is not between 1 and 50 characters in length

def user_profile_setname(token, name_first, name_last):
    """Given active token sets first name, last name and returns empty dict"""
    u_id = verify_token(token)

    if is_invalid_name(name_first):
        raise ValueError("First Name must be between 1 and 50 characters")
    if is_invalid_name(name_last):
        raise ValueError("Last Name must be between 1 and 50 characters")

    user = get_user(u_id)
    change_name(user, name_first, name_last)

    list_of_channels = user['channel']

    for channel_id in list_of_channels:
        channel = find_channel_with_channel_id(channel_id)
        all_members = channel['members']
        owner_members = channel['owner_members']
        for member in all_members:
            if member['u_id'] == u_id:
                change_name(member, name_first, name_last)
        for owner in owner_members:
            if owner['u_id'] == u_id:
                change_name(owner, name_first, name_last)

    return {}

def change_name(user, name_first, name_last):
    """Sets a user's first name and last name for member dict"""
    user['name_first'] = name_first
    user['name_last'] = name_last

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*

# PUT
# user/profile/sethandle
# (token, handle)
# {}

# ValueError when:
# handle must be between 3 and 20 characters
# handle is already used by another user

def user_profile_sethandle(token, handle):
    """Given an active token, sets users handle and return empty dict"""
    verify_token(token)
    if not isinstance(handle, str):
        raise ValueError("Handle must be of type str")
    handle = handle.lower()

    if not is_valid_handle(handle):
        raise ValueError("Invalid Handle length. Handle must be between 3\
                        and 20 characters.")
    if is_used_handle(handle):
        raise ValueError("Handle has been used by another user.")

    users = get_users()
    for user in users:
        if user['token'] == token:
            user['handle_str'] = handle

    return {}
