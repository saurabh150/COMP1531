"""Contains custom exceptions used in server for error handler."""
# This disables the error for overwriting ValueError for our error handler.
# pylint: disable=W0622
from werkzeug.exceptions import HTTPException

# Exceptions to be used in our functions.
class ValueError(HTTPException):
    """Custom ValueError."""
    code = 400
    name = "ValueError"

class AccessError(HTTPException):
    """Custom Access Error for user verification."""
    code = 400
    name = "AccessError"
    description = "Invalid Token"
