"""Contains helper functions used in every other file. Grouped by functionality."""
# This disables the error for overwriting ValueError for our error handler.
# pylint: disable=W0622

import os
import re
from urllib.error import URLError, HTTPError
from requests.exceptions import ConnectionError, MissingSchema
import requests
from .data import get_active_token, get_users, get_channels, get_messages
from .data import get_user, create_member, find_channel_with_channel_id
from .exceptions import ValueError, AccessError

# This file contains all the helper functions needed for other files
#  -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# Auth Function Helpers

def verify_token(token):
    """Check that the token is active. Return u_id. Raise error if inactive token."""
    active_tokens = get_active_token()
    if token in active_tokens:
        users = get_users()
        for user in users:
            if user['token'] == token:
                return user['u_id']
    raise AccessError("Token is currently inactive")

def is_active_token(token):
    """Check if token is currently active. If inactive it raises an access error. Return boolean."""
    active_tokens = get_active_token()
    if token in active_tokens:
        return True
    raise AccessError("Token is currently inactive")

def u_id_exists(u_id):
    """Check if u_id exists. Return boolean."""
    users = get_users()
    for i in users:
        if i['u_id'] == u_id:
            return True
    return False

REGEX = '^\\w+([\\.-]?\\w+)*@\\w+([\\.-]?\\w+)*(\\.\\w{2,3})+$'
def is_invalid_email(email):
    """Verifies email string structure. Return boolean."""
    if re.search(REGEX, email):
        return False
    return True

def is_used_email(email):
    """Check if email has been used. Return boolean."""
    users = get_users()
    for i in users:
        if i['email'] == email:
            return True
    return False

def is_invalid_password(password):
    """Check if password is less than 6 chars. Return boolean."""
    if len(password) < 6:
        return True
    return False

def is_invalid_name(name):
    """Check if name is between 1 and 50 char. Return boolean."""
    if len(name) < 1 or len(name) > 50:
        return True
    return False

def get_user_from_email(email):
    """Return user dict given an email."""
    users = get_users()
    for i in users:
        if email == i['email']:
            return i
    raise ValueError("Email has not been used before")

def get_handle_from_token(token):
    """Return handle given token."""
    u_id = verify_token(token)
    user = get_user(u_id)
    return user['handle_str']


# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# User Profile Helpers

def is_valid_handle(handle):
    """Check that handle is between 3 and 20 chars. Return boolean."""
    if len(handle) > 20 or len(handle) < 3:
        return False
    return True

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# User Profile Upload Photo Helpers

def reset_profile_photo(u_id):
    """
    Checks whether the user originally has a profile image.
    If yes, delete the previous profile image from the database.
    """
    user = get_user(u_id)
    profile_img_url = user['profile_img_url']
    # If there is no profile image, exit function
    if profile_img_url == "":
        return

    # This retrieves the profile image name from the url
    profile_img_name = profile_img_url.split('/')[-1]
    if os.path.exists("img_url/" + profile_img_name):
        os.remove("img_url/" + profile_img_name)
    else:
        raise ValueError("Tried to remove a profile image that doesn't exist")


def verify_url(img_url):
    """Given an image url check whether it is a valid link and return HTTP response."""
    try:
        response = requests.get(img_url)
    except HTTPError:
        raise ValueError("HTTPError. Invalid URL. Could not open")
    except URLError:
        raise ValueError("URLError. Invalid URL. Could not open")
    except ConnectionError:
        raise ValueError("Connection Error. Invalid URL. Could not open.")
    except MissingSchema:
        raise ValueError("Missing Schema Error. Missing http:// or https://")
    if response.status_code != 200:
        raise ValueError("Status Code is not 200. It is " + response.status_code)
    return response

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
def allowed_file(file_format):
    """Check whether file format is an allowed format and return boolean"""
    if file_format.lower() in ALLOWED_EXTENSIONS:
        return True
    return False

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# Channel Helpers

def channel_id_exists(channel_id):
    """Check whether a channel id exists in the list of dicts of channels. Return boolean."""
    channels = get_channels()
    for i in channels:
        if channel_id == i['channel_id']:
            return True
    return False

def verify_token_in_channel(token, channel_id):
    """Check whether a token is active and in the channel. Return boolean or raise error if inactive."""
    if not channel_id_exists(channel_id):
        raise ValueError("Channel Id does not exist.")
    u_id = verify_token(token)
    if not user_is_in_channel(u_id, channel_id):
        raise AccessError("User does not have access to the channel")
    return True

def verify_user_in_channel(user_id, channel_id):
    """Check that a user is in the channel. Raise error if they are not."""
    if not channel_id_exists(channel_id):
        raise ValueError("Channel Id does not exist.")
    if not user_is_in_channel(user_id, channel_id):
        raise AccessError("User does not have access to the channel")

def user_is_in_channel(user_id, channel_id):
    """Check whether a user is in a channel. Return boolean."""
    if not channel_id_exists(channel_id):
        raise ValueError("Channel Id does not exist.")
    user = get_user(user_id)
    user_channels = user['channel']
    if channel_id in user_channels:
        return True
    return False

def channel_add_user(user_id, channel_id):
    """Add a user to a channel in the database. No return value."""
    user = get_user(user_id)
    if user_is_in_channel(user_id, channel_id):
        return

    # Add channel id to user details
    if channel_id not in user["channel"]:
        user["channel"].append(channel_id)

    # Add user id to channel
    channel = find_channel_with_channel_id(channel_id)
    if user_id not in channel["members"]:
        channel["members"].append(create_member(user_id))

def channel_remove_user(user_id, channel_id):
    """Remove user from channel in the database. No return value."""
    # Remove channel id from user
    user = get_user(user_id)
    user["channel"].remove(channel_id)

    # Remove user id from channel
    channel = find_channel_with_channel_id(channel_id)
    channel["members"].remove(create_member(user_id))

def channel_list_users_channels(user_id):
    """Return list of channel dicts a user is part of."""
    channels_out = []
    all_channels = get_channels()

    for channel in all_channels:
        if create_member(user_id) in channel["members"]:
            channels_out.append(channel)

    return channels_out

def user_is_channel_owner(user_id, channel_id):
    """Check if user is channel owner. Return boolean."""
    if create_member(user_id) in find_channel_with_channel_id(channel_id)["owner_members"]:
        return True
    return False

def channel_add_owner(user_id, channel_id):
    """Adds owner member to channel given user_id."""
    find_channel_with_channel_id(channel_id)["owner_members"].append(create_member(user_id))

def channel_remove_owner(user_id, channel_id):
    """Removes owner member from channel given user_id."""
    find_channel_with_channel_id(channel_id)["owner_members"].remove(create_member(user_id))

def channel_make_user_owner_all(user_id):
    """Make user with user_id a member and owner of all channels."""
    user = get_user(user_id)
    all_channels = get_channels()
    for channel in all_channels:
        # Append user_id to channel
        if create_member(user_id) not in channel["members"]:
            channel["members"].append(create_member(user_id))
        if create_member(user_id) not in channel["owner_members"]:
            channel["owner_members"].append(create_member(user_id))

        # Append channel_id to user
        if channel["channel_id"] not in user["channel"]:
            user["channel"].append(channel)

def channel_strip_owner_all(user_id):
    """Given user_id, remove their channel ownership from all channels."""
    all_channels = get_channels()
    for channel in all_channels:
        if create_member(user_id) in channel["owner_members"]:
            channel["owner_members"].remove(create_member(user_id))


# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# Message Helpers

def find_message(message_id):
    """Find message with message_id. Return the message. Raise error if it doesn't exist"""
    messages = get_messages()
    for i in messages:
        if message_id == i['message_id']:
            return i
    raise ValueError("Message with message_id does not exist")

def message_id_exists(message_id):
    """Check whether a message id exists. Return boolean."""
    messages = get_messages()
    for i in messages:
        if message_id == i['message_id']:
            return True
    return False

def is_message_sent_by_user(u_id, message_id):
    """Check whether the message was sent by the user. Return boolean."""
    if not message_id_exists(message_id):
        raise ValueError("Message id doens't exist.")

    messages = get_messages()
    for i in messages:
        if message_id == i['message_id'] and u_id == i['u_id']:
            return True
    return False

def is_user_authorised_to_control_message(u_id, message_id):
    """Check whether the user is authorised to change the message- edit, remove etc.
    Return boolean."""
    message = find_message(message_id)
    channel_id = message['channel_id']
    if is_message_sent_by_user_in_channel(u_id, message_id, channel_id) \
        or user_is_admin(u_id) or user_is_channel_owner(u_id, channel_id):
        return True
    return False

def remove_message_in_channels(message_id, channel_id):
    """Remove message dict from given channel."""
    channel = find_channel_with_channel_id(channel_id)
    messages = channel['messages']
    for i in messages:
        if message_id == i['message_id']:
            messages.remove(i)
            return
    raise ValueError("Message with message_id does not exist")

def is_message_in_channel(message_id, channel_id):
    """Check whether a message is in the channel. Return boolean or raise error
     if message not found."""
    channel = find_channel_with_channel_id(channel_id)
    messages = channel['messages']
    for i in messages:
        if message_id == i['message_id']:
            return True
    raise ValueError("Message id does not exist in the channel given")

def is_message_in_channel_returns_message(message_id, channel_id):
    """Check whether a message is in the channel. Return message dict or raise error
     if message not found."""
    channel = find_channel_with_channel_id(channel_id)
    messages = channel['messages']
    for i in messages:
        if message_id == i['message_id']:
            return i
    raise ValueError("Message id does not exist in the channel given")

def is_message_sent_by_user_in_channel(user_id, message_id, channel_id):
    """Check whether the user is the one who sent the message. Return boolean."""
    message = is_message_in_channel_returns_message(message_id, channel_id)
    if user_id == message['u_id']:
        return True
    return False

def user_get_visible_messages(user_id):
    """Retrieve all visible messages to given user. Return list of message dicts."""
    all_channels = channel_list_users_channels(user_id)
    messages = []
    for channel in all_channels:
        for message in channel["messages"]:
            messages.append(message)
    return messages

# Note this function does not validity checks for whether user has access to the message
def react_append(u_id, message_id, react_id):
    """Add a react to message. Assumes only 1 react id."""
    message = find_message(message_id)
    reacts = message['reacts']
    if reacts == []:
        reacts.append({
            'react_id' : react_id,
            'u_ids' : [u_id]
        })
    else:
        for i in reacts:
            if react_id == i['react_id']:
                u_ids = i['u_ids']
                if u_id in u_ids:
                    raise ValueError("User has already reacted")
                u_ids.append(u_id)


# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# User admin helpers

def user_is_admin(user_id):
    """Check whether a user is an owner/admin of slackr. Return boolean."""
    user = get_user(user_id)
    if user["permission_id"] in [1, 2]:
        return True
    return False

def user_change_permission(user_id, permission_id):
    """Changes a user's permission_id. No return value."""
    user = get_user(user_id)
    user["permission_id"] = permission_id


# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# Standup helpers

def is_active_standup(channel_id):
    """Check whether a channel has an active standup. Return boolean."""
    channel = find_channel_with_channel_id(channel_id)
    return channel['active_standup']


# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
