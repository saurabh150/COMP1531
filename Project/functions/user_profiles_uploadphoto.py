"""
This module allows a user to upload their photo to Slackr as their dp.
"""
# This disables the error for overwriting ValueError for our error handler.
# pylint: disable=W0622, R0913

# Too many arguments
# pylint: disable=R0913

# POST
# user/profiles/uploadphoto (note: this is not requried to be completed
# until iteration 3)
# (token, img_url, x_start, y_start, x_end, y_end)
# {}

# ValueError when:
# img_url is returns an HTTP status other than 200.
# any of x_start, y_start, x_end, y_end are not within the dimensions of
# the image at the URL.


# Given a URL of an image on the internet, crops the image within bounds
# (x_start, y_start) and (x_end, y_end). Position (0,0) is the top left.

# When images are uploaded for a user profile, after processing them you
# should store them on the server such that your server now locally has a
# copy of the cropped image of the original file linked. Then, the
# profile_img_url should be a URL to the server,
# such as http://localhost:5001/imgurl/adfnajnerkn23k4234 (a unique url you generate).

from io import BytesIO
from PIL import Image
from .helper import verify_token, reset_profile_photo, verify_url
from .exceptions import ValueError

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*

# Validation and verification checks on the parameters provided by user
def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    """Retrieve image from url request and return cropped image."""
    u_id = verify_token(token)
    reset_profile_photo(u_id)
    response = verify_url(img_url)
    # Tries to load the image
    try:
        img = Image.open(BytesIO(response.content))
    except OSError:
        raise ValueError("Invalid. Cannot find image in url provided")


    # This is an extra step to check that the file extension is valid.
    # It is not very necessary because it is very hard to find image files
    # not of the types stated.

    # # Checks if the image is in an allowed format
    # if not allowed_file(img.format):
    #     raise ValueError("Invalid image format. Allowed file types are \
    #                         png, jpg, jpeg, gif ")

    max_x, max_y = img.size

    # Validation checks for the input coordinate parameters
    if x_start < 0 or y_start < 0 or x_start >= x_end or y_start >= y_end:
        raise ValueError("Invalid dimensions")

    # ASSUMPTION MADE: CROPPING OVERSIZE JUST CROPS TO ORIGINAL BOUNDARIES
    if x_end > max_x:
        x_end = max_x
    if y_end > max_y:
        y_end = max_y

    # Crops image
    cropped_img = img.crop((x_start, y_start, x_end, y_end))
    return cropped_img
