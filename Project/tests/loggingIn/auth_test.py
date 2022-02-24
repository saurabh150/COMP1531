from functions.auth import auth_passwordreset_reset, auth_passwordreset_request, auth_register, auth_logout, auth_login
import hashlib
from functions.data import get_data, reset_data, get_users
from functions.user_profile import user_profile
from functions.exceptions import ValueError, AccessError
from functions.helper import verify_token
# ----------------------------------------------------------------------------------------------------
# auth_register(email, password, name_first, name_last)
# return: token and u_id

### Erros
# ValueError when invalid/used email and long name_first and name_last, also when invalid password

### Desc:
# User registers with his email so he/she can access services

### Assumptions:
# When a user registeres, an email is sent with confirmation to the user, which will have to be checked
# manually.

# Stub function
# Stub function

reset_data()

# Testing with correct input: Expecting token and u_id
def test_register_correct_input():
    # Setup and Tests
    output = auth_register("saurabh.sir@hotmail.com", "saurabh123456", "Saurabh", "Jain")
    user_profile(output['token'], output['u_id'])

# Testing with incorrect input: Expecting ValueError
def test_register_wrong_input():
    # Tests
    reset_data()
    try:
        # Testing with an invalid password type
        auth_register("notbob@email.com", "123", "Bob", "The Builder")
        assert True == False
    except ValueError:
        print("Passed")

# Testing with used email: Expecting ValueError
def test_register_used_email():
    reset_data()
    # Setup
    email = "saurabh12.sir@hotmail.com"
    # Creating a user with email
    auth_register(email, "123456", "Bob", "The Builder")
    # Tests
    try:
        # attempting to create another user with teh same email
        auth_register(email, "123456", "Bob", "The Builder")
        assert True == False
    except ValueError:
        print("Passed")

# Testing register with invalid email
def test_register_invalid_email():
    reset_data()
    # Setup
    email = "saurabh12.sir@"
    # Creating a user with email
    try:
        auth_register(email, "123456", "Bob", "The Builder")
        assert True == False
    except ValueError:
        print("Passed")

# Testing with long names: Expecting ValueError
def test_register_first_name():
    # Setup
    reset_data()
    nameLong = "Jr__________________________________________________________________________________________________________________________________________________"

    # Tests
    try:
        # Testing with a long name
        auth_register("bob@email.com", "1234567", nameLong,"The Builder")
        assert True == False
    except ValueError:
        print("Passed")

# Testing with long names: Expecting ValueError
def test_register_last_name():
    # Setup
    reset_data()
    nameLong = "Jr__________________________________________________________________________________________________________________________________________________"

    # Tests
    try:
        # Testing with a long name
        auth_register("bob@email.com", "1234567", "hi", nameLong)
        assert True == False
    except ValueError:
        print("Passed")

# ----------------------------------------------------------------------------------------------------

# auth_login(email, password)
# return: token and u_id

### Errors
# Value Error when invalid or unregistered email used, or inccorent password

### Desc:
# Uses registered email and password to login, gets a token so user can access website services

### Assumptions:
# These tests are meant to be run on the actual function, hence might fail at itteration1.
# As the input will be on the website, if the user enters nothing into the fields for email and
# password then it will assume that the input was email:"" and password: "" which are
# invalid password and email.


# Testing with correct input: Checks if the output is correct
def test_login_c_input():
    # Setup
    # Creating a user for testing
    reset_data()
    user1 = auth_register("bob@email.com", "123456", "Bob", "The Builder")
    token1 = user1['token']
    u_id1 = user1['u_id']

    login = auth_login("bob@email.com", "123456")
    tokenFromLogin = login['token']
    u_idFromLogin = login['u_id']

    # checkign if the return values of login adn register are same
    assert tokenFromLogin == token1
    assert u_idFromLogin == u_id1
    u_id_from_token = verify_token(token1)
    assert u_id_from_token == u_id1


# Testing with wrong input: Expected ValueError
def test_login_w_password():
    # Setup
    # Registering a user
    reset_data()
    auth_register("bob1@email.com", "123456", "Bob", "The Builder")

    # Tests
    try:
        # Login with wrong email, should throw an error
        auth_login("bob1@email.com", "not123456")
        assert True == False
    except ValueError:
        print("Passed")

# Testing with unregistered email: Expected ValueError
def test_login_w_email():
    # Setup not required
    reset_data()
    # Tests
    try:
        # login with un-registered email
        auth_login("notbob@emailcom", "123456")
        assert True == False
    except ValueError:
        print("Passed")

# Testing with invalid email: Expected Value
def test_login_invalidEmail():
    # Setup not required
    reset_data()
    # Tests
    try:
        # Testing with wrong email format
        auth_login("bobemail.com", "123456")
        assert True == False
    except ValueError:
        print("Passed")

# Testing with unregistered email
def test_login_unregistered_Email():
    # Setup not required
    reset_data()
    # Tests
    try:
        # Testing with wrong email format
        auth_login("bobemail@hocuspocus.com", "123456")
        assert True == False
    except ValueError:
        print("Passed")


# Testing with wrong input: Expected ValueError
def test_login_w_none():
    # Setup
    reset_data()
    email = ""
    password = ""

    # Tests
    try:
        # testing with wrong email and password format
        auth_login(email, password)
        assert True == False
    except ValueError:
        print("Passed")

# ----------------------------------------------------------------------------------------------------


# auth_logout(token)
# return: {}

### Errors:
# N/A

### Desc:
# The function invalidated the given token so the user logs-out

### Assumptions:
# channels_list has an inccorect token taken care off within the function.

# Test with correct input: Expecting no output
def test_logout_correct():
    # Setup
    reset_data()
    auth_register("bob@email.com", "123456", "Bob", "The Builder")
    login = auth_login("bob@email.com", "123456")
    token = login['token']
    #channel_create(token, "channel1", True)

    # Tests
    assert auth_logout(token)['is_success'] == True
    # As token is invalid, the channels_list must return a empty list
    try:
        verify_token(token)
    except AccessError:
        print("Passed")

# Test with wrong token: Expecting an exception
def test_logout_wrongValue():
    # Setup
    reset_data()
    auth_register("bob1@email.com", "123456", "Bob", "The Builder")
    login = auth_login("bob1@email.com", "123456")
    token = login['token']
    tokenWrong = "Bla_2Bla_2Bla"

    # Tests
    try:
        auth_logout(tokenWrong)
    except AccessError:
        print("PAssed")
    # As token is still valid, the channels_list must return a list which isn't empty
    assert verify_token(token)

# Test with wrong token: Expecting an exception
def test_logout_wrongType():
    # Setup not required
    reset_data
    # Tests
    token = 123.233
    try:
        auth_logout(token)
    except AccessError:
        print("passed")

# ----------------------------------------------------------------------------------------------------

# AUTH PASSWORD RESET TEST
# auth_passwordreset_reset(reset_code, new_password)
# return: None

### Errors:
# ValueError if incorrect resetCode and/or password

### Desc:
# Uses reset code which is sent to an email and new password to make a new password
# for user.

### Assumptions:
# The tests are not properly implemended due to incomplete functions: Reset Code cannot be access automatically
# Have to be checked manually

# Testing with correct input: Expecting no outout
def test_pass_reset_correct_input_reset():
    # Setup: Reset Code has to manually be entered from being sent to a mail
    reset_data()
    email = 'sauabh.sir@hotmail.com'
    auth_register(email, '1234567', 'Saurabh', 'Jain')

    print('output msg',auth_passwordreset_request(email))
    reset_code = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyZXNldF9jb2RlIjoic2F1YWJoLnNpckBob3RtYWlsLmNvbSJ9._0-HZpMKPxBuLkENyXxY9jZEV72tPpwrFVXaK0MrZGE\''
    us = get_users()[0]
    assert us['password'] == hashlib.sha256('1234567'.encode()).hexdigest()
    auth_passwordreset_reset(reset_code, '7654321')
    us = get_users()[0]
    assert us['password'] == hashlib.sha256('7654321'.encode()).hexdigest()

def test_pass_reset_incorrect_reset_code():
    # User already registered
    reset_data()
    email = 'sauabh.sir@hotmail.com'
    auth_register(email, '1234567', 'Saurabh', 'Jain')

    print('output msg',auth_passwordreset_request(email))
    reset_code = 'NOvalidRESETcode'

    us = get_users()[0]
    assert us['password'] == hashlib.sha256('1234567'.encode()).hexdigest()

    try:
        auth_passwordreset_reset(reset_code, '7654321')
    except ValueError:
        print ('passed')

    # Checking if the password is not changed
    us = get_users()[0]
    assert us['password'] == hashlib.sha256('1234567'.encode()).hexdigest()
    #assert us['password'] == hashlib.sha256('1234567'.encode()).hexdigest()

def test_pass_reset_incorrect_password():
    # User already registered
    reset_data()
    email = 'sauabh.sir@hotmail.com'
    auth_register(email, '1234567', 'Saurabh', 'Jain')

    print('output msg',auth_passwordreset_request(email))
    reset_code = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyZXNldF9jb2RlIjoic2F1YWJoLnNpckBob3RtYWlsLmNvbSJ9._0-HZpMKPxBuLkENyXxY9jZEV72tPpwrFVXaK0MrZGE\''

    us = get_users()[0]
    assert us['password'] == hashlib.sha256('1234567'.encode()).hexdigest()

    try:
        auth_passwordreset_reset(reset_code, '')
    except ValueError:
        print ('passed')

    us = get_users()[0]
    assert us['password'] == hashlib.sha256('1234567'.encode()).hexdigest()

# ----------------------------------------------------------------------------------------------------

# PASSWORD RESET REQUEST
# auth_passwordreset_request(email)
# return: {}

### Errors
# N/A

### Desc:
# When a valid email is inputed to this function, an email containing reset code is
# sent to that email

### Assumptions:
# Assuming the if an email is incorrect it doesn't throw any exceptions
# To test look at the email, have to be checked manually

# Testing with correct input: Expecting no output
def test_pass_req_correct_input_reset_request():
    # Setup
    reset_data()
    auth_register("saurabh.sir@hotmail.com", "123456", "Bob", "The Builder")
    email = "saurabh.sir@hotmail.com"

    # Tests
    assert auth_passwordreset_request(email) != None

# Testing with incorrect input: Expecting no output
def test_pass_req_incorrect_input():
    # Setup
    reset_data()
    auth_register("bob@email.com", "123456", "Bob", "The Builder")
    email = "notbob@email"

    # Tests
    assert auth_passwordreset_request(email) == {}

# ----------------------------------------------------------------------------------------------------
