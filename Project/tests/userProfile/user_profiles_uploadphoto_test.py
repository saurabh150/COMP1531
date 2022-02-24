from functions.data import reset_data
from functions.auth import auth_register
from functions.user_profile import user_profile
from functions.user_profiles_uploadphoto import user_profiles_uploadphoto
from functions.exceptions import AccessError, ValueError
from PIL import ImageFile, Image

# user_profile_uploadphoto(token, xStart)
# return: {}

### Errors:
# ValueError when
# img_url is returns an HTTP status other than 200
# x_start, y_start, x_end, y_end are all within the dimensions of the image at the URL

### Desc:
# Given a URL of an image on the internet, crops the image within bounds
# (x_start, y_start) and (x_end, y_end)
# Position (0,0) is the top left.

############### Tests ###############

TOKEN = ""

def setup_tests_upload_photo():
	global TOKEN
	reset_data()
	user = auth_register("bob@email.com", "123456", "Bob", "The Builder")
	TOKEN = user['token']


def test_c_valid_dimensions():
	setup_tests_upload_photo()
	xStart = 100
	xEnd = 200
	yStart = 100
	yEnd = 300
	url = "https://supersimple.com/wp-content/uploads/hello-2-1080-740.jpg"
	image = user_profiles_uploadphoto(TOKEN, url, xStart, yStart, xEnd, yEnd)

	# Uncomment below to visually check that the image has been cropped as expected
	# image.show()
	# Check that the image size has been cropped
	assert image.size == (xEnd - xStart, yEnd - yStart)

# Test cropping dimensions is greater than actual photo. This should return original size of photo
def test_crop_oversize():
	xStart = 0
	xEnd = 2000
	yStart = 0
	yEnd = 3000
	url = "https://supersimple.com/wp-content/uploads/hello-2-1080-740.jpg"
	image = user_profiles_uploadphoto(TOKEN, url, xStart, yStart, xEnd, yEnd)
	assert image.size == (1080, 740)

# Test when start and end values are mixed up
def test_w_start_greater_than_end():
	url = "https://supersimple.com/wp-content/uploads/hello-2-1080-740.jpg"
	xStart = 200
	xEnd = 100
	yStart = 0
	yEnd = 100

	try:
		user_profiles_uploadphoto(TOKEN, url, xStart, yStart, xEnd, yEnd)
		assert True == False
	except ValueError:
		print("Passed")

# Test with negative dimensions
def test_w_negative_dimensions():
	url = "https://supersimple.com/wp-content/uploads/hello-2-1080-740.jpg"
	xStart = -23
	xEnd = 200
	yStart = -12
	yEnd = 100
	try:
		user_profiles_uploadphoto(TOKEN, url, xStart, yStart, xEnd, yEnd)
		assert True == False
	except ValueError:
		print("Passed")

# Test with invalid url
def test_w_invalid_url():
	url = "myphotos.com"
	xStart = 0
	xEnd = 200
	yStart = 0
	yEnd = 100
	try:
		user_profiles_uploadphoto(TOKEN, url, xStart, yStart, xEnd, yEnd)
		assert True == False
	except ValueError:
		print("Passed")

# Test with wrong token
def test_w_wrong_token():
	token = "hello"
	url = "https://supersimple.com/wp-content/uploads/hello-2-1080-740.jpg"
	xStart = 0
	xEnd = 200
	yStart = 0
	yEnd = 200
	try:
		user_profiles_uploadphoto(token, url, xStart, yStart, xEnd, yEnd)
		assert True == False
	except AccessError:
		print("Passed")

# Test with valid url but no photo in url
def test_w_invalid_photo_url():
	url = "https://www.geeksforgeeks.org/working-images-python/"
	xStart = 0
	xEnd = 200
	yStart = 0
	yEnd = 100
	try:
		user_profiles_uploadphoto(TOKEN, url, xStart, yStart, xEnd, yEnd)
		assert True == False
	except ValueError:
		print("Passed")