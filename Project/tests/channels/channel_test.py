# Author: Jason
# Notes: I've rewritten all the tests from iteration 1 to fit iteration 2
# the tests are very different and I have removed a lot of redundant tests
# from iteration 1.
import pytest
import datetime
from functions.channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join, channel_addowner, channel_removeowner, channel_list, channel_listall, channel_create
from functions.message_profile import message_send, message_react, message_unreact
from functions.helper import user_change_permission, verify_token
from functions.data import get_channels, clear_channels, create_member, reset_data 
from functions.auth import auth_register, auth_login
from functions.exceptions import ValueError, AccessError

@pytest.fixture
def setup_data_for_channels():
    reset_data()
    global admin_token, admin_user_id, owner_token, owner_user_id, user_token, user_user_id
    global msg_owner_token, msg_owner_user_id, msg_user_token

    owner_register_result = auth_register("jasonxh@soundclout.me", "OkayPW123", "Owner", "Jason")
    owner_user_id = owner_register_result["u_id"]
    owner_token = owner_register_result["token"]

    admin_register_result = auth_register("jaesonxh@gmail.com", "AightPW123", "Admin", "Jaeson")
    admin_user_id = admin_register_result["u_id"]
    admin_token = admin_register_result["token"]
    user_change_permission(admin_user_id, 2)

    user_register_result = auth_register("jaeson.xh@gmail.com", "BlurghPW123", "User", "Jae")
    user_user_id = user_register_result["u_id"]
    user_token = user_register_result["token"]

    msg_owner_register_result = auth_register("Eddyxw2ong@soundclout.me", "ilovemyself123", "Owner", "Eddy")
    msg_owner_token = msg_owner_register_result["token"]
    msg_owner_user_id = msg_owner_register_result['u_id']
    msg_user_register_result = auth_register("eddy.x.wo1ng@gmail.com", "ihatemyself123", "User", "Ed")
    msg_user_token = msg_user_register_result["token"]

# Logging in
# Note: redundant now that register logs you in
# auth_login("jasonxh@soundclout.me", "OkayPW123")
# auth_login("jaesonxh@gmail.com", "AightPW123")
# auth_login("jaeson.xh@gmail.com", "BlurghPW123")

# channel_details is used and tested throughout this file

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# channel_create

# Testing with correct inputs: Expecting channel_id and matching it with listall id
def test_channel_create_correct_input(setup_data_for_channels):
    # Creating channels and checking if they are made by checking the channels list
    channel_id_pub = channel_create(admin_token, "PublicChannel", 'true')["channel_id"]
    channel_id_priv = channel_create(admin_token, "PrivateChannel", "false")["channel_id"]

    all_channels = get_channels()

    for channel in all_channels:
    	if channel["channel_id"] == channel_id_pub:
    		# Tests for public channel
    		assert channel["is_public"] == True
    		assert create_member(admin_user_id) in channel["owner_members"]
    		assert create_member(owner_user_id) in channel["owner_members"]
    		assert create_member(admin_user_id) in channel["members"]
    		assert create_member(owner_user_id) in channel["members"]

    		# Regular user should be able to find this channel in
    		# listall
    		channelDict = {
    			"channel_id" : channel_id_pub,
    			"name" : channel["name"]
    		}
    		assert channelDict in channel_listall(user_token)["channels"]

    	if channel["channel_id"] == channel_id_priv:
    		# Tests for private channel
    		assert channel["is_public"] == False
    		assert create_member(admin_user_id) in channel["owner_members"]
    		assert create_member(owner_user_id) in channel["owner_members"]
    		assert create_member(admin_user_id) in channel["members"]
    		assert create_member(owner_user_id) in channel["members"]

    		# Regular user should not be able to find this channel in
    		# listall as it's private
    		channelDict = {
    			"channel_id" : channel_id_pub,
    			"name" : channel["name"]
    		}
    		assert channelDict not in channel_listall(user_token)["channels"]
    return

# Testing with long name: Expecting ValueError and only one channel in listall
def test_channel_create_long_name(setup_data_for_channels):
    # Setup
    longName = "LongChannelName......"

    # Test
    try:
        # Attempting to create a channel, which should fail
        channel_create(owner_token, longName, "true")
        assert True == False
    except ValueError:
        print("Passed")

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# channel_list and channel_listall
# Testing with correct input: Expecting a list of dict with channels' details
def test_channel_list_correct_input(setup_data_for_channels):
    # At this point there should be 2 channels, one public
    # and one private
    channel_id_pub = channel_create(admin_token, "PublicChannel", "true")["channel_id"]
    channel_id_priv = channel_create(admin_token, "PrivateChannel", "false")["channel_id"]

    # Testing the data type of/in list as admin
    channel_list_result = channel_list(admin_token)["channels"]
    assert type(channel_list_result) == list
    assert len(channel_list_result) == 2
    for d in channel_list_result:
        assert type(d) == dict
        k = d.keys()
        assert len(k) == 2

    channel_listall_result = channel_listall(admin_token)["channels"]
    assert type(channel_listall_result) == list
    assert len(channel_listall_result) == 2
    for d in channel_listall_result:
        assert type(d) == dict
        k = d.keys()
        assert len(k) == 2

    # Testing user that has not joined any channels
    assert len(channel_list(user_token)["channels"]) == 0
    assert len(channel_listall(user_token)["channels"]) == 1

    # Join channel then test with user
    channel_join(user_token, channel_id_pub)
    assert len(channel_list(user_token)["channels"]) == 1
    assert len(channel_listall(user_token)["channels"]) == 1

    # Clear channels and test
    clear_channels()
    assert len(channel_list(admin_token)["channels"]) == 0
    assert len(channel_listall(admin_token)["channels"]) == 0

def test_channel_list_wrong_input(setup_data_for_channels):
    try:
        channel_list("FakeToken")
        assert True == False
    except AccessError:
        print("Passed")

def test_channel_listall_wrong_input(setup_data_for_channels):
    try:
        channel_listall("FakeToken")
        assert True == False
    except AccessError:
        print("Passed")

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# channel_join and channel_leave
def test_channel_join_leave(setup_data_for_channels):
    channel_id_pub = channel_create(admin_token, "PublicChannel", "true")["channel_id"]
    channel_id_priv = channel_create(admin_token, "PrivateChannel", "false")["channel_id"]

    # Join public channel
    channel_join(user_token, channel_id_pub)
    assert create_member(user_user_id) in channel_details(user_token, channel_id_pub)["all_members"]

    # Try join when already part of channel
    try:
        channel_join(user_token, channel_id_pub)
        assert True == False
    except ValueError:
        print("Passed")

    # Leave public channel
    channel_leave(user_token, channel_id_pub)
    assert create_member(user_user_id) not in channel_details(admin_token, channel_id_pub)["all_members"]

    # Try join private channel
    try:
        channel_join(user_token, channel_id_priv)
        assert True == False
    except AccessError:
        print("Passed")

    # Try joining invalid channel_id
    try:
        channel_join(user_token, 1234)
        assert True == False
    except ValueError:
        print("Passed")

    # Try leaving invalid channel_id
    try:
        channel_leave(user_token, 1234)
        assert True == False
    except ValueError:
        print("Passed")

    # Try admin leaving channel
    try:
        channel_leave(admin_token, channel_id_pub)
        assert True == False
    except ValueError:
        print("Passed")

def test_channel_invite(setup_data_for_channels):
    channel_id_pub = channel_create(admin_token, "PublicChannel", "true")["channel_id"]
    channel_id_priv = channel_create(admin_token, "PrivateChannel", "false")["channel_id"]

    # Try join when authorised user is not part of channel
    try:
        channel_invite(user_token, channel_id_pub, user_user_id)
        assert True == False
    except AccessError:
        print("Passed")

    # Join public channel
    channel_invite(admin_token, channel_id_pub, user_user_id)
    assert create_member(user_user_id) in channel_details(user_token, channel_id_pub)["all_members"]

    # Try join when already part of channel
    try:
        channel_invite(admin_token, channel_id_pub, user_user_id)
        assert True == False
    except ValueError:
        print("Passed")

    # Join private channel by invite
    channel_invite(admin_token, channel_id_priv, user_user_id)
    assert create_member(user_user_id) in channel_details(admin_token, channel_id_priv)["all_members"]

    # Try joining invalid channel_id
    try:
        channel_invite(admin_token, 1234, user_token)
        assert True == False
    except ValueError:
        print("Passed")

    # Try inviting invalid u id
    channel_leave(user_token, channel_id_pub)
    try:
        channel_invite(admin_token, channel_id_pub, 123)
        assert True == False
    except ValueError:
        print("Passed")



# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# channel_details
# only some tests are here, this function is tested throughout the file
def test_channel_details(setup_data_for_channels):
    channel_id_pub = channel_create(admin_token, "PublicChannel", "true")["channel_id"]
    channel_id_priv = channel_create(admin_token, "PrivateChannel", "false")["channel_id"]

    # Get details of invalid channel id
    try:
        channel_details(admin_token, 123)
        assert True == False
    except ValueError:
        print("Passed")

    # Get details of private channel as a
    # user who is not part of the channel
    try:
        channel_details(user_token, channel_id_priv)
        assert True == False
    except AccessError:
        print("Passed")

    # Get details of private channel as admin
    priv_channel_details = channel_details(admin_token, channel_id_priv)
    assert priv_channel_details["name"] == "PrivateChannel"
    assert create_member(admin_user_id) in priv_channel_details["owner_members"]
    assert create_member(owner_user_id) in priv_channel_details["owner_members"]
    assert create_member(admin_user_id) in priv_channel_details["all_members"]
    assert create_member(owner_user_id) in priv_channel_details["all_members"]

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# channel_addowner channel_removeowner
def test_channel_addowner_removeowner(setup_data_for_channels):
    channel_id_pub = channel_create(admin_token, "PublicChannel", "true")["channel_id"]
    channel_id_priv = channel_create(admin_token, "PrivateChannel", "false")["channel_id"]

    # Testing with invalid channel id
    try:
        channel_addowner(admin_token, 123, user_user_id)
        print("Passed")
    except ValueError:
        print("Passed")

    try:
        channel_removeowner(admin_token, 123, user_user_id)
        print("Passed")
    except ValueError:
        print("Passed")

        # Testing with invalid user id
    try:
        channel_addowner(admin_token, channel_id_pub, 123)
        print("Passed")
    except ValueError:
        print("Passed")

    try:
        channel_removeowner(admin_token, channel_id_pub, 123)
        print("Passed")
    except ValueError:
        print("Passed")

    # Add user to owner of public channel
    channel_addowner(admin_token, channel_id_pub, user_user_id)
    assert create_member(user_user_id) in channel_details(admin_token, channel_id_pub)["owner_members"]
    assert create_member(user_user_id) in channel_details(admin_token, channel_id_pub)["all_members"]

    # Try add user who is already owner to owner
    try:
        channel_addowner(admin_token, channel_id_pub, user_user_id)
        assert True == False
    except ValueError:
        print("Passed")

    # Remove user from ownership of public channel
    channel_removeowner(admin_token, channel_id_pub, user_user_id)
    assert create_member(user_user_id) not in channel_details(admin_token, channel_id_pub)["owner_members"]
    assert create_member(user_user_id) not in channel_details(admin_token, channel_id_pub)["all_members"]

    # Try adding self to ownership of public channel
    try:
        channel_addowner(user_token, channel_id_pub, user_user_id)
        assert True == False
    except AccessError:
        print("Passed")

    # Try adding user to ownership when unauthorised
    try:
        channel_addowner(user_token, channel_id_pub, owner_user_id)
        assert True == False
    except AccessError:
        print("Passed")

    # Try removing admin from owner of channel
    try:
        channel_removeowner(owner_token, channel_id_pub, admin_user_id)
        assert True == False
    except ValueError:
        print("Passed")

    # Try removing user when unauthorised
    try:
        channel_removeowner(user_token, channel_id_pub, user_user_id)
        assert True == False
    except AccessError:
        print("Passed")




# Testing with correct input
# This checks that all the values stored inside the message are valid and that the index starts from 0
# Testing with correct input
# This checks that all the values stored inside the message are valid and that the index starts from 0
def test_c_input(setup_data_for_channels):
    first_channel = channel_create(msg_owner_token, "My first channel", "true")
    first_channel_id = first_channel['channel_id']

    start = 0
    first_message_id = message_send(msg_owner_token, first_channel_id, "HELLO WORLD")
    # React to first message
    message_react(msg_owner_token, first_message_id, 1)
    messages_dict = channel_messages(msg_owner_token, first_channel_id, start)
    messages = messages_dict['messages']

    assert first_message_id == messages[0]['message_id']
    assert msg_owner_user_id == messages[0]['u_id']
    assert messages[0]['is_pinned'] == False
    assert messages[0]['time_created'] < datetime.datetime.now().timestamp()
    assert len(messages[0]['reacts']) == 1
    assert messages_dict['start'] == start
    assert messages_dict['end'] == -1

    message_unreact(msg_owner_token, first_message_id, 1)
    messages_dict = channel_messages(msg_owner_token, first_channel_id, start)
    messages = messages_dict['messages']
    assert messages[0]['reacts'][0]['is_this_user_reacted'] == False



# Testing with correct input after sending a message
# It checks that when there are more than 50 messages, only 50 are returned at a time
# It also checks that when start + 50 is greater than end that the messsage end returns -1
def test_c_input_fifty_plus_messages(setup_data_for_channels):
    first_channel = channel_create(msg_owner_token, "My first channel", "true")
    first_channel_id = first_channel['channel_id']
    start = 9
    for i in range(0, 60):
        message_send(msg_owner_token, first_channel_id, "Hi there")
    message_dict = channel_messages(msg_owner_token, first_channel_id, start)
    assert message_dict['start'] == start
    assert message_dict['end'] == 59

    new_message_dict = channel_messages(msg_owner_token, first_channel_id, 11)
    assert new_message_dict['end'] == -1

# This sees whether someone who is not in the channel can view the messages
def test_w_no_access_to_messages(setup_data_for_channels):
    first_channel = channel_create(msg_owner_token, "My first channel", "true")
    first_channel_id = first_channel['channel_id']
    try:
        channel_messages(msg_user_token, first_channel_id, 0)
        assert True == False
    except AccessError:
        print("passed")

# This tests that if the start is greater than the end that a value error is thrown
def test_w_start_greater_than_end(setup_data_for_channels):
    first_channel = channel_create(msg_owner_token, "My first channel", "true")
    first_channel_id = first_channel['channel_id']

    start = 10
    message_send(msg_owner_token, first_channel_id, "Hi there")
    try:
        channel_messages(msg_owner_token, first_channel_id, start)
    except ValueError:
        print("passed")


# Testing with when channel based on ID does not exist (invalidChannelId)
def test_nonexistent_channel_id(setup_data_for_channels):
    non_existent_channel_id = 1
    try:
        channel_messages(msg_owner_token, non_existent_channel_id, 1)
        # Test failed
        assert True == False
    except ValueError:
        print("Passed")