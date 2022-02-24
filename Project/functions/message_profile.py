""" Message profile functions, that contains functions that:
send, send later, remove, react, unreact, pin and unpins"""
# will get rid of this line if standup is not needed
# pylint: disable=W0611,R1720,C0301
# pylint: disable=W0221, R0913, W0102, W0622
import datetime
from threading import Thread
import time as systime
from .helper import verify_token, verify_token_in_channel, is_user_authorised_to_control_message, find_message, remove_message_in_channels, user_is_admin, user_is_channel_owner, react_append
from .exceptions import ValueError, AccessError
from .data import messages_append, get_messages
from .standup import standup_start, standup_active, standup_send

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*

# MESSAGE SEND
# POST
# message/send
# (token, channel_id, message)
# {message_id}

# Send a message from authorised_user to the channel specified by channel_id
def message_send(token, channel_id, message):
    """Send a message given token, channel_id and message"""
    # Error Checking
    if len(message) > 1000:
        raise ValueError("STRING EXCEEDS 1000 CHARACTERS")
    if not isinstance(message, str):
        raise TypeError("Message must be of type string")
    u_id = verify_token(token)
    verify_token_in_channel(token, channel_id)
    # # Standup
    # standup = message.split(" ")
    # if standup[0] == '/standup':
    # 	standup_start(token, channel_id, standup[1])
    # else:
    # 	if standup_active(token, channel_id)['is_active']:
    # 		standup_send(token,channel_id,message)
    message_id = messages_append(u_id, message, channel_id)
    return message_id


# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# MESSAGE SEND LATER
# POST
# (token, channel_id, message, time_sent)
# { message_id }

# Send a message from authorised_user to the channel specified by channel_id automatically at a specified time in the future
def message_sendlater(token, channel_id, message, time_sent):
    """Send a message later, given token, channel_id, message and time"""
    # Assumption time_sent is a datetime object
    # Variable Initialization
    # Error Checking
    if len(message) > 1000:
        raise ValueError("STRING EXCEEDS 1000 CHARACTERS")
	# if time is a time in the past
    curr_time = datetime.datetime.now()

	# the authorised user has not joined the channel they are trying to post to
    verify_token_in_channel(token, channel_id)
    if time_sent <= curr_time:
        raise ValueError("Time sent must be a time in the future")
    date_time_difference = time_sent - curr_time
	# in seconds
    delta_time_in_seconds = date_time_difference.total_seconds()

    message_timer = ThreadWithReturnValue(target=message_send_later_time, args=(token, channel_id, message, delta_time_in_seconds))
    message_timer.start()
    message_id = message_timer.join()
    return {
        'message_id': message_id
    }

# This is a custom class which allows you to start a thread whilst also
# returning a value from the function called.
class ThreadWithReturnValue(Thread):
    """Start a thread while also returning value from function called"""
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

# This is the function called by the ThreadWithReturnValue class which sends a
# message afte a certain time.
def message_send_later_time(token, channel_id, message, time):
    """message send later helper function"""
    systime.sleep(time)
    message_id = message_send(token, channel_id, message)
    return message_id

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# MESSAGE REMOVE
# DELETE
# message/remove
# (token, message_id)
# {}

# ValueError when:
# Message (based on ID) no longer exists

# AccessError when none of the following are true:
# Message with message_id was sent by the authorised user making this request
# The authorised user is an admin or owner of this channel or the slackr

# remove a message
def message_remove(token, message_id):
    """remove message given token and message_id"""
    # Variable initalization
    u_id = verify_token(token)
    if not is_user_authorised_to_control_message(u_id, message_id):
        raise AccessError("User is not authorised to remove this message")

    message = find_message(message_id)
    channel_id = message['channel_id']
    all_messages = get_messages()
    all_messages.remove(message)
    remove_message_in_channels(message_id, channel_id)
    return {}

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# MESSAGE EDIT
# PUT
# (token, message_id, message)
# {}

# Given a message, update it's text with new text
def message_edit(token, message_id, message):
    """edit message given token, message_id and message"""
    u_id = verify_token(token)
    if not is_user_authorised_to_control_message(u_id, message_id):
        raise AccessError("User is not authorised to edit this message")
    message_found = find_message(message_id)
    if message == "":
        message_remove(token, message_id)
    message_found['message'] = message
    return {}

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# MESSAGE PIN
# (token, message_id)
# {}

# Given a message within a channel, mark it as "pinned" to be given special display treatment by the frontend
def message_pin(token, message_id):
    """pin a message given token and message_id"""
	# Initialize Variables
    u_id = verify_token(token)
    message = find_message(message_id)
    channel_id = message['channel_id']
    verify_token_in_channel(token, channel_id)
    if not user_is_admin(u_id) and not user_is_channel_owner(u_id, channel_id):
        raise ValueError("User is not admin and not authorised to pin the message")

    if message['is_pinned'] is True:
    	# message is found but is already unpinned.
        raise ValueError("MESSAGE IS ALREADY PINNED")
    	# if not already un_pinned, unpin it
    else:
        message['is_pinned'] = True
    return {}
# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# MESSAGE UNPIN
# POST
# (token, message_id)
# {}

# Given a message within a channel, remove it's mark as unpinned
def message_unpin(token, message_id):
    """unpin message given token and message_id"""
	# Variable Initialization
    u_id = verify_token(token)
    message = find_message(message_id)
    channel_id = message['channel_id']
    verify_token_in_channel(token, channel_id)
    if not user_is_admin(u_id) and not user_is_channel_owner(u_id, channel_id):
        raise ValueError("User is not admin and not authorised to unpin the message")
    if message['is_pinned'] is False:
    	# message is found but is already unpinned.
        raise ValueError("MESSAGE IS ALREADY UNPINNED")
    	# if not already un_pinned, unpin it
    else:
        message['is_pinned'] = False
    return {}
# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# MESSAGE REACT
# POST
# (token, message_id, react_id)
# {}

# Given a message within a channel the authorised user is part of, add a "react" to that particular message
def message_react(token, message_id, react_id):
    """react to a message given token, message_id and react_id"""
    u_id = verify_token(token)
    message = find_message(message_id)
    channel_id = message['channel_id']
    verify_token_in_channel(token, channel_id)
    if react_id != 1:
        raise ValueError("Invalid react id")
    react_append(u_id, message_id, react_id)
    return {}
# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# POST
# (token, message_id)
# {}

# Given a message within a channel, mark it as "unreacted" to be given special display treatment by the frontend
def message_unreact(token, message_id, react_id):
    """unreact to a message given token, message_id and react_id"""
	# Variable Initialization
    u_id = verify_token(token)
    message = find_message(message_id)
    channel_id = message['channel_id']
    verify_token_in_channel(token, channel_id)
    if react_id != 1:
        raise ValueError("Invalid react_id")
    react = message['reacts']
    for i in react:
        if i['react_id'] == react_id:
            users_reacted = i['u_ids']
            if u_id in users_reacted:
                users_reacted.remove(u_id)
            else:
            # This is under the assumption that there is only 1 possible react_id
                raise ValueError("User has not reacted to this message and can't unreact to it")
    return {}
