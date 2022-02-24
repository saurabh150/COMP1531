import pytest
from functions.search import search_messages
from functions.channel import channel_create, channel_join
from functions.helper import user_change_permission
from functions.exceptions import ValueError, AccessError
from functions.auth import auth_register, auth_login
from functions.message_profile import message_send
from functions.data import get_messages, reset_data

long_query_str = "x"*1005

@pytest.fixture
def setup_data_for_search():
	reset_data()

	# Setting up

	global owner_user_id, owner_token
	global admin_user_id, admin_token
	global user_user_id, user_token
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


def test_search_correct_input(setup_data_for_search):
	# Search when no channels exist
	assert search_messages(admin_token, "test")["messages"] == []

	# Search with

	channel_id_pub = channel_create(admin_token, "PublicChannel", True)["channel_id"]
	channel_id_priv = channel_create(admin_token, "PrivateChannel", False)["channel_id"]

	# Search when no messages are sent
	assert search_messages(admin_token, "test")["messages"] == []

	# Send message in private channel as admin
	message_id = message_send(admin_token, channel_id_priv, "this is a testmessage")

	# Check message in private channel not visible to regular user
	assert search_messages(user_token, "test")["messages"] == []

	# Check message is found and information is there
	result = search_messages(admin_token, "test")["messages"]
	assert len(result) == 1
	assert result[0]["message_id"] == message_id
	assert result[0]["message"] == "this is a testmessage"
	assert result[0]["u_id"] == admin_user_id
	assert result[0]["is_pinned"] == False
	assert result[0]["reacts"] == []

	# Send message in public channel
	message_send(admin_token, channel_id_pub, "another message")
	# Check message in public channel is visible to someone in it
	flag = 0
	for message in search_messages(admin_token, "another")["messages"]:
		if message["message"] == "another message":
			flag = 1

	assert flag == 1

	# Check message in public channel is not visible to regular user yet
	assert search_messages(user_token, "another")["messages"] == []

	# Join channel then find message
	channel_join(user_token, channel_id_pub)
	result = search_messages(user_token, "another")["messages"]
	assert len(result) == 1
	assert result[0]["message"] == "another message"

	# Test with unauthorised token
	try:
		search_messages("aaaa", "another")
		assert True == False
	except AccessError:
		print("Passed")

def test_search_long_query():
	try:
		search_messages(admin_token, long_query_str)
		assert True == False
	except ValueError:
		print("Passed")