"""This module contains the userpermission change function."""
# This disables the error for overwriting ValueError for our error handler.
# pylint: disable=W0622
from .helper import user_is_admin, user_change_permission
from .helper import verify_token, channel_strip_owner_all, channel_make_user_owner_all
from .data import get_user
from .exceptions import AccessError, ValueError

def admin_userpermission_change(token, user_id, permission_id):
    """Change a user's permission level. Return {}"""
    # Verify token
    admin_user_id = verify_token(token)
    admin_user_permission_id = get_user(admin_user_id)['permission_id']
    prev_permission = get_user(user_id)["permission_id"]

    # Check authorised user is admin or owner
    if not user_is_admin(admin_user_id):
        raise AccessError("Authorised user is not admin or owner of slackr")

    # Check permission id is valid
    if permission_id not in [1, 2, 3]:
        raise ValueError("Permission ID does not refer to a value permission")

    # NOTE: ASSUMING PERMISSION ID CAN'T BE 1, OWNER if user who called is also not a OWNER
    if permission_id == 1 and admin_user_permission_id != 1:
        raise ValueError("Can not change permission to owner")

    # Check permission is actually being changed
    if prev_permission == permission_id:
        raise ValueError("Permission is already " + str(permission_id))

    # Check permission of user being changed isn't owner
    if prev_permission == 1 and admin_user_permission_id != 1:
        raise ValueError("Can not change permission of owner")

    # Change permission of user
    user_change_permission(user_id, permission_id)

    # If 1->2, make user owner and member of every channel
    if prev_permission == 3 and permission_id in [1, 2]:
        channel_make_user_owner_all(user_id)

    # If 2->1, strip user of all channel ownership
    if prev_permission in [1, 2] and permission_id == 3:
        channel_strip_owner_all(user_id)
    return {}
