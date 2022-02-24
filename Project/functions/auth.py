"""This module contains functions related to log in, log out, reset pass code,
register."""
# This disables the error for overwriting ValueError for our error handler.
# pylint: disable=W0622, R1710
import hashlib
import jwt
from .exceptions import ValueError
from .data import get_users, get_active_token, users_append
from .helper import is_invalid_email, is_invalid_name, is_invalid_password
from .helper import is_used_email, is_active_token, get_user_from_email

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# POST
# auth/register
# (email, password, name_first, name_last)
# { u_id, token }

# ValueError when:
# Email entered is not a valid email using the method provided here
# (unless you feel you have a better method).
# Email address is already being used by another user
# Password entered is less than 6 characters long
# name_first not is between 1 and 50 characters in length
# name_last is not between 1 and 50 characters in length


# Given a user's first and last name, email address, and password,
# create a new account for them and return a new token for authentication
# in their session. A handle is generated that is the concatentation of a
# lowercase-only first name and last name. If the concatenation is longer
# than 20 characters, it is cutoff at 20 characters. If the handle is already
# taken, you may modify the handle in any way you see fit to make it unique.

# Function which generates a token from the u_id which is provided
def token_generator(data):
    """Return a new token."""
    token = jwt.encode({'u_id':data}, '', algorithm='HS256')
    return str(token)

def auth_register(email, password, name_first, name_last):
    """Create a new user. Return new user token and u_id."""
    # Error Checking
    if is_invalid_email(email):
        raise ValueError("Invalid Email")

    if is_used_email(email):
        raise ValueError("Email has been used before")

    if is_invalid_password(password):
        raise ValueError("Invalid Password")

    if is_invalid_name(name_first):
        raise ValueError("First name must be between 1 and 50 characters")

    if is_invalid_name(name_last):
        raise ValueError("Last name must be between 1 and 50 characters")

    # Storing the data
    users = get_users()
    u_id = len(users) + 1
    token = token_generator(u_id)

    # Adding the user to the data structure of users
    users_append(email, hashlib.sha256(password.encode()).hexdigest(), \
                name_first, name_last, u_id, token)

    # Adding user token to active token
    active_tokens = get_active_token()
    active_tokens.append((token))
    # Return
    return {
        'u_id' : u_id,
        'token' : token
    }

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# POST
# auth/login
# (email, password)
# { u_id, token }

# ValueError when:
# Email entered is not a valid email using the method provided here
# (unless you feel you have a better method)
# Email entered does not belong to a user
# Password is not correct


# Given a registered users' email and password and generates a valid token
#  for the user to remain authenticated

def auth_login(email, password):
    """Log the user in. Return user Token and u_id."""
    # Setting up data structure
    users = get_users()

    # Checking if valid input
    if is_invalid_email(email):
        raise ValueError("Invalid Email")

    if not is_used_email(email):
        raise ValueError("Unregistered Email")

    # Loggingin
    active_tokens = get_active_token()

    # Comparing  and looking for the user with the email provided
    for user in users:
        if user['email'] == email:
            if user['password'] == hashlib.sha256(password.encode()).hexdigest():\
                # If email and password match proceed further
                u_id = user['u_id']
                token = user['token']
                active_tokens = get_active_token()
                active_tokens.append(token)
                return {
                    'u_id' : u_id,
                    'token' : token
                }
            # If email matchs and password doesn't then incorrect password  enetered
            raise ValueError("Incorrect Password")

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# POST
# auth/logout
# (token)
# { is_success }
# N/A
# Given an active token, invalidates the taken to log the user out.
# If a valid token is given, and the user is successfully logged out,
# it returns true, otherwise false.

def auth_logout(token):
    """Log the user out. Return boolean for logout success."""
    # Setting up the data  structure
    active_token = get_active_token()
    #  Checking if the token is active, will raise an error if not active in the function itself
    is_active_token(token)
    # removinf the token from active token
    active_token.remove(token)

    return {
        'is_success' : True
    }

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# POST
# auth/passwordreset/request
# (email)
# {}
# Given an email address, if the user is a registered user, send's them
# a an email containing a specific secret code, that when entered in
# auth_passwordreset_reset, shows that the user trying to reset the password
# is the one who got sent this email.

def auth_passwordreset_request(email):
    """Generate a reset password code. Return a message to be sent to user's email."""
    # If an unused email is enetered, will just return {}
    if not is_used_email(email):
        return {}

    # Generating a reset code
    reset_code = jwt.encode({'reset_code':email}, '', algorithm='HS256')
    reset_code = str(reset_code)
    # Generating the email message with the reset code
    message = (f'Dear user,\n Your reset code to reset your password is:\n \
        {reset_code}\n Enter this code in the password reset page. If you did \
            not try and reset your password, please disregard this message.\n\n \
                Kind Regards,\nTeam Slackr.')
    user = get_user_from_email(email)
    # This sets the user reset_code in the global dictionary
    user['reset_code'] = reset_code
    # Returns the msg to be sent to the users email from the APP
    return message


# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# POST
# auth/passwordreset/reset
# (reset_code, new_password)
# {}
# Given a reset code for a user, set that user's new password to the password provided.
# If a Valid reset code is provided along with valid new_password,
# will return {} but updates users password
# Incorrect reset code and invalid password will raise ValueError

# Returns the  email of the user whose reset code it is
def decode_reset_code(reset_code):
    """Decode reset code. Return user's email."""
    users = get_users()
    for user in users:
        if user['reset_code'] == reset_code:
            return user['email']
    raise ValueError('Email not found')

def auth_passwordreset_reset(reset_code, new_password):
    """Reset the password. Returns {}"""
    user_email = decode_reset_code(reset_code)
    user_to_update = get_user_from_email(user_email)
    # Checking password validity
    if is_invalid_password(new_password):
        raise ValueError("Invalid password")
    # Updating data structure
    user_to_update['password'] = hashlib.sha256(new_password.encode()).hexdigest()
    user_to_update['reset_code'] = None
    return {}
