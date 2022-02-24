"""Individual message_sendlater_tests"""
# pylint: disable=W0622, C0301
import pytest
from datetime import datetime, timedelta
from functions.message_profile import message_sendlater
from functions.auth import auth_register, auth_logout
from functions.exceptions import ValueError, AccessError
from functions.helper import find_message
from functions.channel import channel_create, channel_join
from functions.data import reset_data
# Send a message from authorised_user to the channel specified by channel_id automatically at a specified time in the future

OWNER_U_ID = -1
OWNER_TOKEN = ""
USER_USER_ID = -1
USER_TOKEN = ""
NONUSER_USER_ID = -1
NONUSER_TOKEN = ""
GLOBAL_CHANNEL_ID = -1

@pytest.fixture
def setup_data_messages():
    global OWNER_U_ID, OWNER_TOKEN, USER_TOKEN, USER_USER_ID
    global NONUSER_USER_ID, NONUSER_TOKEN, GLOBAL_CHANNEL_ID
    reset_data()

    # Setting up
    OWNER_REGISTER_RESULT = auth_register("Eddyx3wong@soundclout.me", "ilovemyself123", "Owner", "Eddy")
    OWNER_U_ID = OWNER_REGISTER_RESULT["u_id"]
    OWNER_TOKEN = OWNER_REGISTER_RESULT["token"]

    USER_REGISTER_RESULT = auth_register("eddy.x2.wong@gmail.com", "ihatemyself123", "User", "Ed")
    USER_USER_ID = USER_REGISTER_RESULT["u_id"]
    USER_TOKEN = USER_REGISTER_RESULT["token"]

    NONUSER_REGISTER_RESULT = auth_register("nonuser@1gmail.com", "ihatemyself123", "nonuser", "Ed")
    NONUSER_USER_ID = NONUSER_REGISTER_RESULT["u_id"]
    NONUSER_TOKEN = NONUSER_REGISTER_RESULT["token"]

    # Setting up global channel
    GLOBAL_CHANNEL_ID = channel_create(OWNER_TOKEN, "PublicChannel", True)["channel_id"]

    # Joining Channels
    channel_join(USER_TOKEN, GLOBAL_CHANNEL_ID)
# Tests
# check if message is sent later
# I should be able to check if message is sent later
# THe testing for the actual message content is minimal because it is tested in
# message send
def test_message_send_later(setup_data_messages):
    """Message_send_later correct operation"""
    owner_message = "I iz owner"
    time_in_future = datetime.now() + timedelta(seconds=5)
    owner_message_id = message_sendlater(OWNER_TOKEN, GLOBAL_CHANNEL_ID, owner_message, time_in_future)['message_id']
    message = find_message(owner_message_id)
    assert datetime.fromtimestamp(message['time_created']) - time_in_future < timedelta(milliseconds=100)
    assert message['message'] == owner_message

# check if message length is invalid
def test_message_send_in_past():
    """Message_send_later send a message in the past"""
    owner_message = "hallo"
    time_in_past = datetime.now() - timedelta(minutes=5)
    try:
        message_sendlater(OWNER_TOKEN, GLOBAL_CHANNEL_ID, owner_message, time_in_past)
        assert True is False
    except ValueError:
        print("passed")

def test_message_send_no_access():
    """Message_send_later no access"""
    random_message = "hallo"
    time_in_future = datetime.now() + timedelta(seconds=5)
    try:
        message_sendlater(NONUSER_TOKEN, GLOBAL_CHANNEL_ID, random_message, time_in_future)
        assert True is False
    except AccessError:
        print("passed")

def test_message_send_1001_characters():
    """Message_send_later character length exceeds 1000"""
    random_message = "x" * 1001
    time_in_future = datetime.now() + timedelta(seconds=5)
    try:
        message_sendlater(OWNER_TOKEN, GLOBAL_CHANNEL_ID, random_message, time_in_future)
        assert True is False
    except ValueError:
        print("passed")

def test_message_send_inactive_token():
    """Message_send_later has an inactive token"""
    auth_logout(OWNER_TOKEN)
    random_message = "x" * 100
    time_in_future = datetime.now() + timedelta(seconds=5)
    try:
        message_sendlater(OWNER_TOKEN, GLOBAL_CHANNEL_ID, random_message, time_in_future)
        assert True is False
    except AccessError:
        print("passed")
