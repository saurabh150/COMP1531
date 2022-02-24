import pytest
from functions.auth import auth_register, auth_login
from functions.exceptions import ValueError, AccessError
from functions.admin import admin_userpermission_change
from functions.helper import user_is_admin, user_change_permission
from functions.data import reset_data

@pytest.fixture
def setup_data_for_permchange():
	reset_data()
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


def test_admin_userpermission_change_invalid_token(setup_data_for_permchange):
	# Try invalid token
	try:
		admin_userpermission_change("token", user_user_id, 2)
		assert True == False
	except AccessError:
		print("Passed")

def test_admin_userpermission_change_owner(setup_data_for_permchange):
	# Try changing owner permission
	try:
		admin_userpermission_change(admin_token, owner_user_id, 2)
		assert True == False
	except ValueError:
		print("Passed")

# Try invalid permission id
def test_admin_userpermission_change_invalid_pid(setup_data_for_permchange):
	try:
		admin_userpermission_change(admin_token, user_user_id, 4)
		assert True == False
	except ValueError:
		print("Passed")

# Try changing to admin when user is already admin
def test_admin_userpermission_change_same(setup_data_for_permchange):
	try:
		admin_userpermission_change(owner_token, admin_user_id, 2)
		assert True == False
	except ValueError:
		print("Passed")

# Try invalid uid
def test_admin_userpermission_invalid_uid(setup_data_for_permchange):
	try:
		admin_userpermission_change(owner_token, 123, 2)
		assert True == False
	except ValueError:
		print("Passed")

# Try change permission of regular user as regular user
def test_admin_userpermission_unauth_token(setup_data_for_permchange):
	try:
		admin_userpermission_change(user_token, user_user_id, 2)
		assert True == False
	except AccessError:
		print("Passed")

# Try changing user to owner when authorised user is only an admin
def test_admin_userpermission_make_owner_w(setup_data_for_permchange):
	try:
		admin_userpermission_change(admin_token, user_user_id, 1)
		assert True == False
	except ValueError:
		print("Passed")

# Change user to admin
def test_admin_userpermission_make_admin(setup_data_for_permchange):
	admin_userpermission_change(owner_token, user_user_id, 2)
	assert user_is_admin(user_user_id) == True

	# Try setting admin to admin again
	try:
		admin_userpermission_change(owner_token, user_user_id, 2)
		assert True == False
	except ValueError:
		print("Passed")

# Change admin to user
def test_admin_userpermission_demote_admin(setup_data_for_permchange):
	admin_userpermission_change(owner_token, admin_user_id, 3)
	assert user_is_admin(user_user_id) == False