"""Contains search_messages function."""
# This disables the error for overwriting ValueError for our error handler.
# pylint: disable=W0622
from .helper import user_get_visible_messages, verify_token
from .exceptions import ValueError

def search_messages(token, query_str):
    """Search all messages a user can view for string. Return the message."""
    # Check length of query_str
    if len(query_str) > 1000:
        raise ValueError("Query string too long")

    # Verify token and retrieve user id
    user_id = verify_token(token)
    result_messages = []

    lists_of_messages = user_get_visible_messages(user_id)
    for message in lists_of_messages:
        if query_str in message["message"]:
            result_messages.append(message)
    return {"messages" : result_messages}
