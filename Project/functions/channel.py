"""This module contains all the functions relevant to channels. This includes
channel invite, create, remove owner, add owner, leave, details, messages, list,
listall, join."""
# This disables the error for overwriting ValueError for our error handler.
# pylint: disable=W0622, R1703
from .data import get_channels, channel_append, get_users, find_channel_with_channel_id
from .helper import verify_token_in_channel, channel_add_user, channel_remove_user
from .helper import channel_list_users_channels, user_is_channel_owner, channel_add_owner
from .helper import channel_remove_owner, verify_token, channel_id_exists
from .helper import verify_user_in_channel, u_id_exists, user_is_admin, user_is_in_channel
from .exceptions import AccessError, ValueError

def channel_invite(token, channel_id, user_id):
    """Invites a user to a channel."""
    # Token verification
    auth_user_id = verify_token(token)

    # Checking inputs are valid
    if not channel_id_exists(channel_id):
        raise ValueError("Channel ID does not exist")

    verify_user_in_channel(auth_user_id, channel_id)
    if user_is_in_channel(user_id, channel_id):
        raise ValueError("User is already in the channel. Cannot invite.")

    # Add user to channel
    channel_add_user(user_id, channel_id)
    return {}

def channel_details(token, channel_id):
    """Returns the details in a channel."""
    # Token verification and user id retrieval
    user_id = verify_token(token)

    # Verify channel ID exists
    if not channel_id_exists(channel_id):
        raise ValueError("Channel ID is not a valid channel")

    # Check the user is part of the channel
    channel = find_channel_with_channel_id(channel_id)
    if not channel['is_public']:
        verify_user_in_channel(user_id, channel_id)

    return {
        "name" : channel["name"],
        "owner_members" : channel["owner_members"],
        "all_members" : channel["members"]
    }

# GET
# channel/messages
# (token, channel_id, start)
# { messages, start, end }

# ValueError when:
# Channel ID is not a valid channel
# start is greater than or equal to the total number of messages in the channel

# AccessError when
# Authorised user is not a member of channel with channel_id

# What are messages:
# (outputs only) named exactly messages
# List of dictionaries, where each dictionary contains types
# { message_id, u_id, message, time_created, reacts, is_pinned, }

# Given a Channel with ID channel_id that the authorised user is part of,
# return up to 50 messages between index "start" and "start + 50".
# Message with index 0 is the most recent message in the channel.
# This function returns a new index "end" which is the value of "start + 50",
# or, if this function has returned the least recent messages in the channel,
# returns -1 in "end" to indicate there are no more messages to load after this return.

def channel_messages(token, channel_id, start):
    """Shows a list of the most recent messages. Returns dictionary of messages and start, end."""
    u_id = verify_token(token)
    verify_token_in_channel(token, channel_id)

    channel = find_channel_with_channel_id(channel_id)
    messages = channel['messages']
    new_messages_list = [{k: v for k, v in d.items() if k != 'channel_id'} for d in messages]
    # This loops through every message in the list to check whether the current user has
    # reacted to it
    for message in new_messages_list:
        reacts = message['reacts']
        for react in reacts:
            users_reacted = react['u_ids']
            if u_id in users_reacted:
                react['is_this_user_reacted'] = True
            else:
                react['is_this_user_reacted'] = False
    end = -1
    if start + 50 >= len(messages):
        return {
            'messages': new_messages_list[start:],
            'start': start,
            'end' : end
        }
    end = start + 50
    return {
        'messages': new_messages_list[start:end],
        'start': start,
        'end' : end
    }

def channel_leave(token, channel_id):
    """Allows user to leave a channel. Return {}."""
    # Verify token
    user_id = verify_token(token)

    # Check inputs are valid
    if not channel_id_exists(channel_id):
        raise ValueError("Channel ID is not a valid channel.")
    verify_user_in_channel(user_id, channel_id)
    if user_is_admin(user_id):
        raise ValueError("Admins cannot leave a channel.")

    # Remove user
    channel_remove_user(user_id, channel_id)
    return {}

def channel_join(token, channel_id):
    """Allows user to join a public channel. Return {}."""
    # Verify token
    user_id = verify_token(token)
    if not channel_id_exists(channel_id):
        raise ValueError("Channel ID is not a valid channel")
    channel = find_channel_with_channel_id(channel_id)
    # Verify channel is public
    if not channel["is_public"]:
        raise AccessError("Channel ID is not a valid channel (private)")

    if user_is_in_channel(user_id, channel_id):
        raise ValueError("User is already in channel")

    channel_add_user(user_id, channel_id)
    return {}

def channel_addowner(token, channel_id, user_id):
    """Adds an owner to a channel. Return {}."""
    # Verify token
    admin_user_id = verify_token(token)

    # Check valid inputs
    if not channel_id_exists(channel_id):
        raise ValueError("Channel ID is not a valid channel")
    if not u_id_exists(user_id):
        raise ValueError("User ID is not a valid user")
    if not user_is_channel_owner(admin_user_id, channel_id):
        raise AccessError("The user is not an owner of the channel. They cannot add an owner.")

    # Check if user is already owner of channel
    if user_is_channel_owner(user_id, channel_id):
        raise ValueError("User is already owner of channel")

    # Add new owner
    channel_add_owner(user_id, channel_id)
    channel_add_user(user_id, channel_id)
    return {}

def channel_removeowner(token, channel_id, user_id):
    """Removes an owner from a channel. Return {}."""
    # Verify token
    verify_token(token)

    # Check valid inputs
    if not channel_id_exists(channel_id):
        raise ValueError("Channel ID is not a valid channel")
    if not u_id_exists(user_id):
        raise ValueError("User ID is not a valid user")

    # Check if user is owner of channel
    if not user_is_channel_owner(user_id, channel_id):
        raise AccessError("User is not an owner of the channel. Cannot remove them as owner.")

    # Check if user is administrator
    if user_is_admin(user_id):
        raise ValueError("Cannot remove an owner who is an administrator of slackr")

    # Remove owner
    channel_remove_owner(user_id, channel_id)
    channel_remove_user(user_id, channel_id)
    return {}

def channel_list(token):
    """Lists all the channels a user is a part of. Returns a dict of these channels."""
    # Verify token and get user id
    user_id = verify_token(token)

    list_channels = channel_list_users_channels(user_id)
    channels_out = []

    for channel in list_channels:
        channels_out.append({
            "channel_id" : channel["channel_id"],
            "name" : channel["name"]
        })

    return {"channels" : channels_out}

def channel_listall(token):
    """Lists all the channels a user can access. Returns dict of channels."""
    user_id = verify_token(token)
    channels_out = []
    all_channels = get_channels()
    if user_is_admin(user_id):
        # List all channels
        for channel in all_channels:
            channels_out.append({
                "channel_id" : channel["channel_id"],
                "name" : channel["name"]
            })
    else: # Not admin
        for channel in all_channels:
            if channel["is_public"]:
                channels_out.append({
                    "channel_id" : channel["channel_id"],
                    "name" : channel["name"]
                })

    return {"channels" : channels_out}

def channel_create(token, name, is_public):
    """Creates a new channel and makes creator the owner. Returns a dict with channel_id."""
    if len(name) > 20:
        raise ValueError("Name is too long (more than 20 characters)")

    # Convert is_public from string to boolean
    if is_public in ('true', True):
        is_public = True
    else:
        is_public = False

    user_id = verify_token(token)
    channel_id = channel_append(name, user_id, is_public)

    # Make all admins and owner part of new channel
    all_users = get_users()
    for user in all_users:
        if user["permission_id"] in [1, 2]:
            channel_add_user(user["u_id"], channel_id)
            channel_add_owner(user["u_id"], channel_id)

    return {"channel_id" : channel_id}
