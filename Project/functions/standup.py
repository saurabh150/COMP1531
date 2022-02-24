"""This module contains all functions related to standups. Includes standup start,
startup send, standup active."""
# Disabling errors for overwriting ValueError internal function and inconsistent returns.
# pylint: disable=W0622, R1710
import datetime
import threading
from .exceptions import ValueError
from .data import get_channels, standup_messages_append, messages_append
from .data import find_channel_with_channel_id
from .helper import verify_token, verify_token_in_channel
from .helper import is_active_standup, get_handle_from_token
# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# POST
# standup/start
# (token, channel_id)
# { time_finish }

# ValueError when:
# Channel ID is not a valid channel
# An active standup is currently running in this channel

# AccessError whenThe authorised user is not a member of the channel that
# the message is within

# For a given channel, start the standup period whereby for the next 15 minutes
# if someone calls "standup_send" with a message, it is buffered during the 15
# minute window then at the end of the 15 minute window a message will be added
# to the message queue in the channel from the user who started the standup.

def standup_start(token, channel_id, length):
    """Start standup in a channel. Returns time standup finishes."""
    # Verifying input
    if is_active_standup(channel_id):
        raise ValueError("There is currently an active standup already.")
    verify_token_in_channel(token, channel_id)
    length = float(length)

    # Using timer structure to manupulate with message delays
    time_start = datetime.datetime.now()
    time_finish = time_start + datetime.timedelta(seconds=length)
    time_stamp = time_finish.timestamp()
    #replace(tzinfo=timezone.utc).timestamp()

    # Set a 'length' second long timer to send the messages

    timer_standup = threading.Timer(length, end_standup)
    timer_standup.start()

    channel = find_channel_with_channel_id(channel_id)
    # Activiating Standup in the channel
    channel.update({
        'active_standup' : True,
        'standup_activator' : token,
        'standup_time_start' : time_start.timestamp(),
        'standup_time_finish' : time_stamp
    })

    return {'time_finish' : time_stamp}


# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*

def end_standup():
    """Ends the standup by posting the messages. Returns message_id."""
    for channel in get_channels():
        if channel['active_standup'] and \
            datetime.datetime.now().timestamp() > channel['standup_time_finish']:
            msg = ""
            standup_messages = channel['standup_messages']
            # Setting up temp variables
            for message in standup_messages:
                name = get_handle_from_token(message['token'])
                message_user = message['message']
                # Adding all messages to one message string
                msg += f'{name}: {message_user}\n'
            # Sending the message as a thread of one message - assuming it
            # doesn't exceed length of message
            token = channel['standup_activator']
            channel_id = channel['channel_id']
            u_id = verify_token(token)
            verify_token_in_channel(token, channel_id)

            message_id = messages_append(u_id, msg, channel_id)

            # Reseting the standup in the channel
            channel.update({
                'standup_messages' : [],
                'standup_activator' : None,
                'standup_time_start' : None,
                'standup_time_finish' : None,
                'active_standup' : False
            })

            return message_id

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# POST
# standup/send
# (token, channel_id, message)
# {}

# ValueError when:
# Channel ID is not a valid channel
# Message is more than 1000 characters
# An active standup is not currently running in this channel

# AccessError whenThe authorised user is not a member of the channel that the message is within

# Sending a message to get buffered in the standup queue, assuming a standup is currently active


def standup_send(token, channel_id, message):
    """Store the messages into standup msg dict. Returns {}."""
    # Verification
    if not is_active_standup(channel_id):
        raise ValueError("There is no active standup")
    verify_token_in_channel(token, channel_id)
    if len(message) > 1000:
        raise ValueError("STRING EXCEEDS 1000 CHARACTERS")

    # Just appending the message to send to the standup messages data structure
    standup_messages_append(token, channel_id, message)

    return {}

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*

def standup_active(token, channel_id):
    """ Checks if standup is active | Returns is_active and time_finish """
    verify_token_in_channel(token, channel_id)

    return_values = {
        'is_active' : False,
        'time_finish' : None
    }

    channel = find_channel_with_channel_id(channel_id)
    if channel['active_standup']:
        return_values = {
            'is_active' : True,
            'time_finish' : channel['standup_time_finish']
        }
    return return_values
