# This disables the error for overwriting ValueError for our error handler.
# pylint: disable=W0622

import pytest
from functions.auth import auth_register
from functions.user_profile import user_profile, user_profile_setemail
from functions.user_profile import user_profile_setname, user_profile_sethandle
from functions.exceptions import AccessError, ValueError
from functions.users_all import users_all
from functions.data import reset_data
from functions.channel import channel_create, channel_details

# user_profile_setemail(token, email)
# return: {}

### Errors:
# ValueError when
# Email entered is not a valid email
# Email address is already being used by another user

### Desc:
# Update the authorised user's email address


### Assumptions ###
# wrong token = value error
# For used emails- go to database to check

VALID_U_ID = -1
VALID_TOKEN = ""
VALID_U_ID_2 = -1
VALID_TOKEN_2 = ""
GLOBAL_CHANNEL_ID = -1

@pytest.fixture
def setup_tests_user_profile():
    reset_data()
    global VALID_U_ID, VALID_U_ID_2, VALID_TOKEN, VALID_TOKEN_2, GLOBAL_CHANNEL_ID
    registered = auth_register("user8@email.com", "UserPassword", "Molly", "Thompson")
    registered2 = auth_register("users9@email.com", "UserPassword", "Jack", "Thompson")
    VALID_U_ID = registered["u_id"]
    VALID_TOKEN = registered["token"]
    VALID_U_ID_2 = registered2['u_id']
    VALID_TOKEN_2 = registered2['token']
    # Setting up global channel
    GLOBAL_CHANNEL_ID = channel_create(VALID_TOKEN_2, "PublicChannel", True)["channel_id"]



############### Tests ###############
# USER PROFILE TESTS
# Tests correct input
def test_c_return(setup_tests_user_profile):
    assert user_profile(VALID_TOKEN, VALID_U_ID) == {"email" : "user8@email.com",\
    "name_first" : "Molly", "name_last" : "Thompson", \
        "handle_str" : "mollythompson", "profile_img_url": ""}

# Tests invalid input wrong type uId
def test_w_invalid_u_id():
    invalid_u_id = 8
    try:
        user_profile(VALID_TOKEN, invalid_u_id)
        assert True is False
    except ValueError:
        print("Passed")

# Tests input with None
def test_w_none():
    try:
        user_profile(None, None)
        assert True is False
    except ValueError:
        print("Passed")

# Tests input with empty strings
def test_w_empty_string():
    try:
        user_profile("", 0)
        assert True is False
    except ValueError:
        print("Passed")

# SETEMAIL TESTS

# Test valid email. Then test if email was changed
def test_c_valid_email():
    email = "lookAtMe@hello.com"
    assert user_profile_setemail(VALID_TOKEN, email) == {}

    user = user_profile(VALID_TOKEN, VALID_U_ID)
    assert email is user['email']

# Test invalid email with space
def test_w_invalid_email_with_space():
    email = "lookAt Me@hello.com"
    try:
        user_profile_setemail(VALID_TOKEN, email)
        assert True is False
    except ValueError:
        print("Passed")

# Test invalid email with speechmarck
def test_w_invalid_email_with_speechmark():
    email = "lookAt'Me@hello.com"
    try:
        user_profile_setemail(VALID_TOKEN, email)
        assert True is False
    except ValueError:
        print("Passed")

# Test invalid email without @ symbol
def test_w_invalid_email_without_at():
    email = "lookAhello.com"
    try:
        user_profile_setemail(VALID_TOKEN, email)
        assert True is False
    except ValueError:
        print("Passed")

# Test invalid email ends with @
def test_w_invalid_email_ends_at():
    email = "lookAhello.com@"
    try:
        user_profile_setemail(VALID_TOKEN, email)
        assert True is False
    except ValueError:
        print("Passed")

# Test with used email
def test_w_used_email():
    email = "users9@email.com"
    try:
        user_profile_setemail(VALID_TOKEN, email)
        assert True is False
    except ValueError:
        print("Passed")

# Test email wrong tokem
def test_w_valid_email_wrong_token():
    token = "12345"
    email = "lookAhello@imcool.com"
    try:
        user_profile_setemail(token, email)
        assert True is False
    except AccessError:
        print("Passed")

# Test email with None
def test_w_none_email():
    email = None
    try:
        user_profile_setemail(VALID_TOKEN, email)
        assert True is False
    except TypeError:
        print("Passed")


# SetHandle Tests

# Testing with valid inputs and that user_profile was actually changed
def test_c_valid_handle():
    handle = "hello"
    assert user_profile_sethandle(VALID_TOKEN, handle) == {}

    profile = user_profile(VALID_TOKEN, VALID_U_ID)
    assert handle == profile['handle_str']

#  Test with handle set to over 20 characters
def test_w_invalid_handle_excess_characters():
    handle = "lasdfhalkjhwekjdhfkajshdkfhajksz"
    try:
        user_profile_sethandle(VALID_TOKEN, handle)
        assert True is False
    except ValueError:
        print("Passed")

#  Test invalid type
def test_w_invalid_handle_integer():
    handle = 1234
    try:
        user_profile_sethandle(VALID_TOKEN, handle)
        assert True is False
    except ValueError:
        print("Passed")

# Test with trying to set handle but have wrong token
def test_w_valid_handle_wrong_token():
    token = "12345"
    handle = "iamcool"
    try:
        user_profile_sethandle(token, handle)
        assert True is False
    except AccessError:
        print("Passed")

def test_w_used_handle():
    try:
        user_profile_sethandle(VALID_TOKEN, "jackthompson")
        assert True is False
    except ValueError:
        print("Passed")

# SETNAME TESTS

# Test setting valid name. Checks that name is actually set
def test_c_valid_name():
    name_first = "Amy"
    name_last = "Smith"
    assert user_profile_setname(VALID_TOKEN_2, name_first, name_last) == {}

    profile = user_profile(VALID_TOKEN_2, VALID_U_ID_2)
    assert profile['name_first'] is name_first
    assert profile['name_last'] is name_last
    # Check name has been changed in the channel
    details = channel_details(VALID_TOKEN_2, GLOBAL_CHANNEL_ID)
    owners = details['owner_members']
    all_members = details['all_members']
    for member in owners:
        if member['u_id'] == VALID_U_ID_2:
            assert member['name_first'] == name_first
            assert member['name_last'] == name_last
        break
    for member in all_members:
        if member['u_id'] == VALID_U_ID_2:
            assert member['name_first'] == name_first
            assert member['name_last'] == name_last
        break


# Test valid name with spaces
def test_c_valid_name_with_spaces():
    name_first = "i'm crazy"
    name_last = "Smith"
    assert user_profile_setname(VALID_TOKEN_2, name_first, name_last) == {}

    profile = user_profile(VALID_TOKEN_2, VALID_U_ID_2)
    assert profile['name_first'] is name_first
    assert profile['name_last'] is name_last

# Test name_first too many letters
def test_w_long_first_name():
    name_first = "Some times in our lives, we all have pain, we all have sorrow.\
        But if you are wise, you know that there's always tomorrow."
    name_last = "Johnson"
    try:
        user_profile_setname(VALID_TOKEN, name_first, name_last)
        assert True is False
    except ValueError:
        print("Passed")

# Test name_last too many letters
def test_w_long_last_name():
    name_first = "happy"
    name_last = "Someday I wish upon a star, and wake up where the clouds are far\
        behind me. Where troubles melt like lemon drops away above the chimneytops\
            that's where you'll find me."
    try:
        user_profile_setname(VALID_TOKEN, name_first, name_last)
        assert True is False
    except ValueError:
        print("Passed")

# Test with None
def test_w_none_name():
    try:
        user_profile_setname(VALID_TOKEN, None, None)
        assert True is False
    except TypeError:
        print("Passed")

# Test with empty strings
def test_w_empty_string_name():
    try:
        user_profile_setname(VALID_TOKEN, "", "")
        assert True is False
    except ValueError:
        print("Passed")

# Test with wrong token
def test_w_token():
    token = "12345"
    try:
        user_profile_setname(token, "hello", "i'm tired")
        assert True is False
    except AccessError:
        print("Passed")

# Testing users_all
def test_users_all():
    print(users_all(VALID_TOKEN))
    all_users = users_all(VALID_TOKEN)
    assert all_users == {
        'users':[{
            'email':'lookAtMe@hello.com',
            'u_id': 1,
            'name_first':'Molly',
            'name_last':'Thompson',
            'handle_str':'hello',
            'profile_img_url':''
        }, {
            'email':'users9@email.com',
            'u_id': 2,
            'name_first':"i'm crazy",
            'name_last':'Smith',
            'handle_str':'jackthompson',
            'profile_img_url':''
        }]
    }
