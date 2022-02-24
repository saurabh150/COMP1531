"""MESSAGE PROFILE TESTING"""
# pylint: disable=W0622, C0301
import pytest
from functions.message_profile import find_message, message_send, message_remove, message_edit, message_pin, message_unpin, message_react, message_unreact
from functions.auth import auth_register
from functions.exceptions import ValueError, AccessError
from functions.channel import channel_create, channel_join
from functions.admin import admin_userpermission_change
from functions.data import get_channels, get_data, reset_data

M_OWNER_U_ID = -1
M_OWNER_TOKEN = ""
M_ADMIN_USER_ID = -1
M_ADMIN_TOKEN = ""
M_USER_USER_ID = -1
M_USER_TOKEN = ""
NONUSER_USER_ID = -1
NONUSER_TOKEN = ""
M_GLOBAL_CHANNEL_ID = -1

@pytest.fixture
def setup_data_messages():
    global M_OWNER_U_ID, M_OWNER_TOKEN, M_ADMIN_USER_ID, M_ADMIN_TOKEN, M_USER_TOKEN
    global M_USER_USER_ID, NONUSER_USER_ID, NONUSER_TOKEN, M_GLOBAL_CHANNEL_ID
    reset_data()

    M_OWNER_REGISTER_RESULT = auth_register("Eddyxwo3ng@soundclout.me", "ilovemyself123", "Owner", "Eddy")
    M_OWNER_U_ID = M_OWNER_REGISTER_RESULT["u_id"]
    M_OWNER_TOKEN = M_OWNER_REGISTER_RESULT["token"]

    M_ADMIN_REGISTER_RESULT = auth_register("eddyxw2ong@gmail.com", "plsloveme123", "Admin", "Edd")
    M_ADMIN_USER_ID = M_ADMIN_REGISTER_RESULT["u_id"]
    M_ADMIN_TOKEN = M_ADMIN_REGISTER_RESULT["token"]
    admin_userpermission_change(M_OWNER_TOKEN, M_ADMIN_USER_ID, 2)

    M_USER_REGISTER_RESULT = auth_register("eddy.x.4wong@gmail.com", "ihatemyself123", "User", "Ed")
    M_USER_USER_ID = M_USER_REGISTER_RESULT["u_id"]
    M_USER_TOKEN = M_USER_REGISTER_RESULT["token"]

    NONUSER_REGISTER_RESULT = auth_register("nonus2er@gmail.com", "ihatemyself123", "nonuser", "Ed")
    NONUSER_USER_ID = NONUSER_REGISTER_RESULT["u_id"]
    NONUSER_TOKEN = NONUSER_REGISTER_RESULT["token"]

    # Setting up global channel

    M_GLOBAL_CHANNEL_ID = channel_create(M_ADMIN_TOKEN, "PublicChannel", "true")["channel_id"]

    # Joining Channels
    channel_join(M_USER_TOKEN, M_GLOBAL_CHANNEL_ID)



# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# message_send
# token, channel_id, message
# messsage_id
# Testing with correct inputs: Expecting a message_id and checking with find_message is correct
def test_message_send_correct_output(setup_data_messages):
    """message_send correct output"""
    # SETUP
    owner_message = "I iz owner"
    print(M_GLOBAL_CHANNEL_ID)
    print(get_data())
    owner_message_id = message_send(M_OWNER_TOKEN, M_GLOBAL_CHANNEL_ID, owner_message)

    assert(find_message(owner_message_id)['message']) == "I iz owner"

# Testing with incorrect inputs: MessageId does not exist
def test_message_send_incorrect_output():
    """message_send incorrect output"""
    # SETUP
    owner_message_id = 1

    try:
        find_message(owner_message_id)
        assert True is False
    except ValueError:
        print("Passed")

# Testing when message has 1000+ characters
def test_message_send_1001_characters():
    """message_send exceeds 1000 characters"""
    message = "x" * 1001

    try:
        message_send(M_OWNER_TOKEN, M_GLOBAL_CHANNEL_ID, message)
        assert True is False
    except ValueError:
        print("Passed")

# Testing when user has not joined channel
def test_message_send_user_has_not_joined_channel():
    """message_send, user not in channel"""
    message = "hallo"

    try:
        message_send(NONUSER_TOKEN, M_GLOBAL_CHANNEL_ID, message)
        assert True is False
    except AccessError:
        print("Passed")

# Testing when sending a non string
def test_message_send_wrong_type():
    try:
        message_send(NONUSER_TOKEN, M_GLOBAL_CHANNEL_ID, [])
        assert True == False
    except TypeError:
        print("Passed")

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# Message Remove
# token, message_id
# {}

# Given a message_id for a message, this message is removed from the channel
def test_message_remove_correct_output():
    """message remove correct operation"""
    owner_message = "I iz owner"
    owner_message_id = message_send(M_OWNER_TOKEN, M_GLOBAL_CHANNEL_ID, owner_message)

    message_remove(M_OWNER_TOKEN, owner_message_id)

    try:
        find_message(owner_message_id)
        assert True is False
    except ValueError:
        print("Passed")


# Message with message_id was not sent by the authorised user making this request
# The authorised user is not an admin or owner of this channel or the slackr
def test_message_remove_when_user_is_not_admin_or_owner():
    """message_remove when user is not an admin or owner"""
    user_message = "I iz annoyed"
    user_message_id = message_send(M_OWNER_TOKEN, M_GLOBAL_CHANNEL_ID, user_message)

    # User is not an admin or owner or the user who sent this request
    try:
        message_remove(M_USER_TOKEN, user_message_id)
        assert True is False
    except AccessError:
        print("Passed")

# Remove a message that doesn't exist at all
def test_message_remove_correct_message_doesnt_exist():
    """message_remove when message doesn't exist"""
    owner_message_id = 1

    try:
        find_message(owner_message_id)
        assert True is False
    except ValueError:
        print("Passed")
# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# Message Edit
# token, message_id, message
# {}

# Correctly edit a message
def test_message_edit_correct_output():
    """message_edit correct output"""
    message = "I like trains"
    message_id = message_send(M_OWNER_TOKEN, M_GLOBAL_CHANNEL_ID, message)

    new_message = "I like turtles"
    message_edit(M_OWNER_TOKEN, message_id, new_message)

    test_message = find_message(message_id)
    found_message_str = test_message['message']
    print(found_message_str)
    assert found_message_str == "I like turtles"

# no change to message
def test_message_not_edited():
    """message_edit no change to message"""
    message = "I like trains"
    message_id = message_send(M_OWNER_TOKEN, M_GLOBAL_CHANNEL_ID, message)

    test_message = find_message(message_id)
    assert test_message['message'] != "I like turtles"

# user has no access to message
def test_message_not_admin():
    """message_edit when user has no access to message"""
    message = "I like trains"
    token = M_OWNER_TOKEN
    channel = M_GLOBAL_CHANNEL_ID

    message_id = message_send(token, channel, message)
    new_message = "I like turtles"
    try:
        message_edit(M_USER_TOKEN, message_id, new_message)
        assert True is False
    except AccessError:
        print("passed")

# message inputed is an empty string
def test_message_no_string():
    """message_edit empty string operation"""
    message = "what is lyfe"
    message_id = message_send(M_OWNER_TOKEN, M_GLOBAL_CHANNEL_ID, message)

    new_message = ""
    message_edit(M_OWNER_TOKEN, message_id, new_message)
    try:
        find_message(message_id)
        assert True is False
    except ValueError:
        print("passed")

#   -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# Message Pin
# token, message_id
# {}
def test_message_pin_correct():
    """message_pin is correctly pinned"""
    message = "I like trains"
    message_id = message_send(M_OWNER_TOKEN, M_GLOBAL_CHANNEL_ID, message)

    message_pin(M_OWNER_TOKEN, message_id)

    assert(is_message_pinned(message_id)) is True

def test_message_pin_already_pinned():
    """message_pin is already pinned"""
    message = "I like trains"
    message_id = message_send(M_OWNER_TOKEN, M_GLOBAL_CHANNEL_ID, message)
    message_pin(M_OWNER_TOKEN, message_id)
    try:
        message_pin(M_OWNER_TOKEN, message_id)
        assert True is False
    except ValueError:
        print("passed")

def test_message_pin_no_access():
    """message_pin has no access"""
    message = "I like trains"
    message_id = message_send(M_OWNER_TOKEN, M_GLOBAL_CHANNEL_ID, message)
    try:
        message_pin(M_USER_TOKEN, message_id)
        assert True is False
    except ValueError:
        print("passed")

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# MESSAGE UNPIN
# token, message_id
# {}

# Given a message within a channel, remove it's mark as unpinned
def test_message_unpin_correct():
    """message_unpin correctly unpins"""
    message = "I like trains"
    message_id = message_send(M_OWNER_TOKEN, M_GLOBAL_CHANNEL_ID, message)

    message_pin(M_OWNER_TOKEN, message_id)
    message_unpin(M_OWNER_TOKEN, message_id)

    assert(is_message_pinned(message_id)) is False


def test_message_unpin_already_pinned():
    """message_unpin unpins an already unpinned message"""
    message = "I like trains"
    message_id = message_send(M_OWNER_TOKEN, M_GLOBAL_CHANNEL_ID, message)

    message_pin(M_OWNER_TOKEN, message_id)
    message_unpin(M_OWNER_TOKEN, message_id)

    try:
        message_unpin(M_OWNER_TOKEN, message_id)
        assert True is False
    except ValueError:
        print("passed")


def test_message_unpin_no_access():
    """message_unpin has no access to message"""
    message = "I like trains"
    message_id = message_send(M_OWNER_TOKEN, M_GLOBAL_CHANNEL_ID, message)

    message_pin(M_OWNER_TOKEN, message_id)

    try:
        message_unpin(M_USER_TOKEN, message_id)
        assert True is False
    except ValueError:
        print("passed")

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# Message React
# POST
# (token, message_id, react_id)
# {}

def test_message_react_correct_output():
    """message_react correctly reacts to message"""
    message = "I like trains"
    message_id = message_send(M_OWNER_TOKEN, M_GLOBAL_CHANNEL_ID, message)

    message_react(M_OWNER_TOKEN, message_id, 1)
    assert(is_message_reacted(M_OWNER_U_ID, message_id, 1)) is True

def test_message_react_wrong_id():
    message = "I like trains"
    message_id = message_send(M_OWNER_TOKEN, M_GLOBAL_CHANNEL_ID, message)

    try:
        message_react(M_OWNER_TOKEN, message_id, 3)
        assert True == False
    except ValueError:
        print("Passed")

def test_message_react_no_react():
    """message_react has no react"""
    message = "I like trains"
    message_id = message_send(M_OWNER_TOKEN, M_GLOBAL_CHANNEL_ID, message)

    assert(is_message_reacted(M_OWNER_U_ID, message_id, 1)) is False

def test_message_react_already_reacted():
    """message_react has already reacted"""
    message = "I like trains"
    message_id = message_send(M_OWNER_TOKEN, M_GLOBAL_CHANNEL_ID, message)
    message_react(M_OWNER_TOKEN, message_id, 1)

    try:
        message_react(M_OWNER_TOKEN, message_id, 1)
        assert True is False
    except ValueError:
        print("passed")

def test_message_react_no_access():
    """message_react has no access"""
    message = "I like trains"
    message_id = message_send(M_OWNER_TOKEN, M_GLOBAL_CHANNEL_ID, message)

    # to test if user has access
    try:
        message_react(NONUSER_TOKEN, message_id, 1)
        assert True is False
    except AccessError:
        print("passed")
#-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# Message Unreact
# (token, message_id)
# {}

def test_message_unreact_correct():
    """message_unreact has correctly unreacted a message"""
    message = "I like trains"
    message_id = message_send(M_OWNER_TOKEN, M_GLOBAL_CHANNEL_ID, message)
    message_react(M_OWNER_TOKEN, message_id, 1)

    message_unreact(M_OWNER_TOKEN, message_id, 1)
    assert(is_message_reacted(M_OWNER_U_ID, message_id, 1)) is False

def test_message_unreact_already():
    """message_unreact has already unreacted a message"""
    message = "I like trains"
    message_id = message_send(M_OWNER_TOKEN, M_GLOBAL_CHANNEL_ID, message)
    message_react(M_OWNER_TOKEN, message_id, 1)

    message_unreact(M_OWNER_TOKEN, message_id, 1)
    try:
        message_unreact(M_OWNER_TOKEN, message_id, 1)
        assert True is False
    except ValueError:
        print("passed")

def test_message_unreact_no_access():
    """message_unreact has no access to message"""
    message = "I like trains"
    message_id = message_send(M_OWNER_TOKEN, M_GLOBAL_CHANNEL_ID, message)

    # to test if user has access
    try:
        message_unreact(NONUSER_TOKEN, message_id, 1)
        assert True is False
    except AccessError:
        print("passed")

# did not write one for react
def test_message_unreact_not_valid_react_id():
    """message_unreact has an invalid react_id"""
    message = "I like trains"
    message_id = message_send(M_OWNER_TOKEN, M_GLOBAL_CHANNEL_ID, message)

    # to test if user has access
    try:
        message_unreact(M_OWNER_TOKEN, message_id, 2)
        assert True is False
    except ValueError:
        print("passed")
#-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# TINY HELPER FUNCTION TO MAKE CODE CLEANER
def is_message_pinned(message_id):
    """helper function to check if message is pinned"""
    message = find_message(message_id)
    if message['is_pinned'] is True:
        return True
    return False

def is_message_reacted(u_id, message_id, react_id):
    """helper function to check if message is reacted"""
    message = find_message(message_id)
    react_list = message['reacts']
    for i in react_list:
        users_reacted = i['u_ids']
        if i['react_id'] == react_id and u_id in users_reacted:
            return True
    return False
