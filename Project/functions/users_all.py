"""Contains users_all function."""
from .data import get_users
from .helper import verify_token

def users_all(token):
    """Return list of all users in a dict."""
    verify_token(token)
    users_out = []
    all_users = get_users()

    for user in all_users:
        # email, name_first, name_last, handle_str, profile_img_url
        users_out.append({
            "email" : user["email"],
            "u_id" : user["u_id"],
            "name_first" : user["name_first"],
            "name_last" : user["name_last"],
            "handle_str" : user["handle_str"],
            "profile_img_url" : user["profile_img_url"]
        })

    return {"users" : users_out}
