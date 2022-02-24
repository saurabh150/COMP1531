"""API and DATA functions"""
# too many arguments
# pylint: disable=R0913

# disabling global statement pylint
# pylint: disable=W0603

# we redefined ValueError so we have an error handler
# pylint: disable=W0622

import uuid
import datetime
from math import log10, floor
import os
import pickle
import string_utils
from .exceptions import ValueError

DATA = {
    'users' : [],
    'channels' : [],
    'messages' : [],
    'active_tokens' : []
    }

def set_data():
    """Looks for pickled file, if not data is initalized."""
    global DATA
    if os.path.exists('stored_DATA.p'):
        DATA = pickle.load(open("stored_DATA.p", "rb")) # alternative way
    else:
        DATA = {
            'users' : [],
            'channels' : [],
            'messages' : [],
            'active_tokens' : []
        }
    # Creates a directory for profile images
    if not os.path.exists('img_url'):
        os.mkdir('img_url')

def save_data():
    """Save global data structure by pickling it and storing it on harddisk."""
    global DATA
    # print(DATA)
    with open('stored_data.p', 'wb') as file:
        pickle.dump(DATA, file)


def reset_data():
    """Reset global data structure."""
    global DATA
    DATA = {
        'users' : [],
        'channels' : [],
        'messages' : [],
        'active_tokens' : []
        }

# ID HELPERS
# u_id here is unique identifier thx
def reset_id(u_id):
    """Reset id helper function. Returns a u_id"""
    u_id = round(u_id, 15-int(floor(log10(abs(u_id))))-1)
    while u_id > 100000000000000:
        u_id = u_id/10
    u_id = int(u_id)
    return u_id

### API ###
def get_data():
    """API function, gets global data. Returns global data."""
    global DATA
    return DATA

def get_users():
    """API function, gets users. Returns users."""
    global DATA
    return DATA['users']

def get_channels():
    """API function, gets channels. Returns channels."""
    global DATA
    return DATA['channels']

def get_messages():
    """API function, gets messages. Returns messages"""
    global DATA
    return DATA['messages']

def get_active_token():
    """API function, gets active token. Returns active tokens"""
    global DATA
    return DATA['active_tokens']

def get_standup_messages():
    """API function, gets stand up messages. Returns standup messages"""
    global DATA
    return DATA['standup_messages']

def clear_channels():
    """API function, gets channels list and clears it."""
    global DATA
    DATA["channels"] = []
    all_users = get_users()
    for user in all_users:
        user["channel"] = []

def clear_messages():
    """API function, get message_list and clears it."""
    global DATA
    DATA['messages'] = []
    all_channels = get_channels()
    for i in all_channels:
        i['messages'] = []

def standup_messages_append(token, channel_id, message):
    """API function, adds a new standup message to channel dict"""
    channels = get_channels()
    for channel in channels:
        if channel['channel_id'] == channel_id:
            standup_messages = channel['standup_messages']
            standup_messages.append({
                'token' : token,
                'message' : message
            })

def users_append(email, password, name_first, name_last, u_id, token):
    """API function, creates new user and adds to global user list."""
    users = get_users()
    permission_id = 3

    # For the first user to joing slackr, they will be an owner
    if len(users) == 0:
        permission_id = 1

    users.append({
        'email' : email,
        'password' : password,
        'name_first' : name_first,
        'name_last' : name_last,
        'u_id' : u_id,
        'token' : token,
        'handle_str' : generate_handle(name_first, name_last),
        'channel' : [],
        'permission_id' : permission_id,
        'reset_code' : None,
        'profile_img_url': ""
        })

def add_profile_image(token, image_name, port):
    """API function, adds a profile picture to user dictionary"""
    users = get_users()
    url = "http://localhost:" + port + "/img_url/" + image_name
    channel_ids = []
    u_id = 0
    for user in users:
        if user['token'] == token:
            user['profile_img_url'] = url
            channel_ids = user['channel']
            u_id = user['u_id']

    if u_id == 0:
        raise ValueError("Unable to find user i        add_profile_image function")

    for channel_id in channel_ids:
        channel = find_channel_with_channel_id(channel_id)
        owner_members = channel['owner_members']
        all_members = channel['members']
        for owner in owner_members:
            if owner['u_id'] == u_id:
                owner['profile_img_url'] = url
        for member in all_members:
            if member['u_id'] == u_id:
                member['profile_img_url'] = url


def find_channel_with_channel_id(channel_id):
    """API function, finds a channel in channel list. Returns given channel dict"""
    channels = get_channels()
    for i in channels:
        if channel_id == i['channel_id']:
            return i
    raise ValueError("Channel Id does not exist")

# Returns a dictionary with the u_id, first name and last name of a member
def create_member(u_id):
    """API function, creates a user. Returns a dict of the user"""
    users = get_users()
    for i in users:
        if i['u_id'] == u_id:
            return {
                'u_id' : u_id,
                'name_first': i['name_first'],
                'name_last' : i['name_last'],
                'profile_img_url' : i['profile_img_url']
            }
    raise ValueError("User id provided doesn't exist")

# Creates a new channel but also adds the channel to the user's DATA
# Returns the new channel_id generated
def channel_append(name, owner_u_id, is_public):
    """API function, creates a new channel and appends to global channel list. Returns channel_id"""
    channels = get_channels()
    new_channel_id = len(channels) + 1
    channels.append({
        'name' : name,
        'messages' : [],
        'channel_id' : new_channel_id,
        'members': [create_member(owner_u_id)],
        'owner_members' : [create_member(owner_u_id)],
        'is_public': is_public,
        'active_standup': False,
        'standup_activator' : None,
        'standup_time_start' : None,
        'standup_time_finish' : None,
        'standup_messages' : []
    })

    users = get_users()
    for i in users:
        if owner_u_id == i['u_id']:
            i['channel'].append(new_channel_id)
            return new_channel_id
    raise ValueError("User provided should be in the global list    of users")

# Appends to list of messages but also the list of messages inside a channel
# Returns the new message_id generated
def messages_append(u_id, message, channel_id):
    """API function, Makes message dict, appends to global message list. Returns message_id"""
    messages = get_messages()
    channel = find_channel_with_channel_id(channel_id)
    new_message_id = uuid.uuid1().int
    new_message_id = reset_id(new_message_id)
    new_message = {
        'message_id': new_message_id,
        'u_id': u_id,
        'message': message,
        'time_created': datetime.datetime.now().timestamp(),
        'reacts': [],
        'is_pinned': False,
        'channel_id': channel_id
    }
    messages.insert(0, new_message)
    # Adding to list of messages in channel
    channel['messages'].insert(0, new_message)
    return new_message_id

# Helper function that retrieves user dictionary given user_id
def get_user(user_id):
    """Helper function, gets user dict given user_id. Returns user dict"""
    all_users = get_users()
    for user in all_users:
        if user['u_id'] == user_id:
            return user
    raise ValueError("User ID does not refer to a valid user")

# This generates a new handle by concatenating first and last name.
# If the handle is not unique, it shuffles the letters around in the string
def generate_handle(name_first, name_last):
    """Helper function, makes a handle name given first and last name. Returns handle"""
    handle = name_first.lower() + name_last.lower()
    if len(handle) > 20:
        handle = handle[0:19]
    if is_used_handle(handle):
        while is_used_handle(handle):
            handle = string_utils.shuffle(handle)
    return handle

# Checks whether the handle has been used by another user
def is_used_handle(handle):
    """Helper function, checks if another user has given handle. Returns boolean True or False"""
    users = get_users()
    for i in users:
        if i['handle_str'] == handle:
            return True
    return False
