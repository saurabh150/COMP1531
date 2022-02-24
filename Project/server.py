"""Flask server"""
import sys
import os
import jwt
import uuid
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from json import dumps
from flask import Flask, request, jsonify
from functions import user_profile, user_profiles_uploadphoto
from functions import message_profile
from functions import auth
from functions import helper
from functions import standup
from functions import channel
from functions import search
from functions import users_all
from functions import admin
from flask_mail import Mail, Message
from functions import data
import threading
import datetime

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# This is an exception handler. With this in place, the exception will be handled
# nicely by the frontend.

data.set_data()

def save_data_():
	timer = threading.Timer(1.0,save_data_)
	timer.start()
	data.save_data()
save_data_()

def defaultHandler(err):
	response = err.get_response()
	response.data = dumps({
		"code": err.code,
		"name": err.name,
		"message": err.description,
	})
	response.content_type = 'application/json'
	return response

APP = Flask(__name__, static_folder='img_url')
APP.secret_key = "secret key"
APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)
CORS(APP)

UPLOAD_FOLDER = os.getcwd() + "/img_url"
APP.config.update(
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'slackoverflow1@gmail.com',
	MAIL_PASSWORD = "notJustPassword1234",
	UPLOAD_FOLDER= UPLOAD_FOLDER,
	MAX_CONTENT_LENGTH= 16 * 1024 * 1024
)

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# LOGGING IN FUNCTIONS
@APP.route('/auth/register', methods=['POST'])
def register():
	email = request.form.get('email')
	password = request.form.get('password')
	name_first = request.form.get('name_first')
	name_last = request.form.get('name_last')
	result = auth.auth_register(email, password, name_first, name_last)
	return dumps(result)

@APP.route('/auth/login', methods=['POST'])
def login():
	email = request.form.get('email')
	password = request.form.get('password')
	result = auth.auth_login(email, password)
	return dumps(result)

@APP.route('/auth/logout', methods=['POST'])
def logout():
	token = request.form.get('token')
	result = auth.auth_logout(token)
	return dumps(result)

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# POST
# auth/passwordreset/request
# (email)
# {}
# Given an email address, if the user is a registered user, send's them a an
# email containing a specific secret code, that when entered in
# auth_passwordreset_reset, shows that the user trying to reset the
# password is the one who got sent this email.

@APP.route('/auth/passwordreset/request', methods=['POST'])
def passwordreset_request():
	email = request.form.get('email')
	message = auth.auth_passwordreset_request(email)
	if message == {}:
		return dumps({})

	mail = Mail(APP)
	try:
		msg = Message("Slackr Password Reset Verification",
						sender="slackoverflow1@gmail.com",
						recipients=[email])
		msg.body = message
		mail.send(msg)
		return dumps({})
	except Exception as e:
		return str(e)


@APP.route('/auth/passwordreset/reset', methods=['POST'])
def password_reset():
	reset_code = request.form.get('reset_code')
	new_password = request.form.get('new_password')
	auth.auth_passwordreset_reset(reset_code,new_password)
	return dumps({})


# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# USER PROFILE FUNCTIONS
@APP.route('/users/all', methods=['GET'])
def get_all_users():
	token = request.args.get('token')
	result = users_all.users_all(token)
	return dumps(result)

@APP.route('/user/profile', methods=['GET'])
def get_user_profile():
	token = request.args.get('token')
	u_id = int(request.args.get('u_id'))
	result = user_profile.user_profile(token, u_id)
	return dumps(result)

@APP.route('/user/profile/setemail', methods=['PUT'])
def set_email():
	token = request.form.get('token')
	email = request.form.get('email')
	result = user_profile.user_profile_setemail(token, email)
	return dumps(result)

@APP.route('/user/profile/setname', methods=['PUT'])
def change_name():
	token = request.form.get('token')
	name_first = request.form.get('name_first')
	name_last = request.form.get('name_last')
	result = user_profile.user_profile_setname(token, name_first, name_last)
	return dumps(result)

@APP.route('/user/profile/sethandle', methods=['PUT'])
def change_handle():
	token = request.form.get('token')
	handle = request.form.get('handle')
	result = user_profile.user_profile_sethandle(token, handle)
	return dumps(result)

@APP.route('/user/profiles/uploadphoto', methods=['POST'])
def upload_photo():
	token = request.form.get('token')
	img_url = request.form.get('img_url')
	x_start = int(request.form.get('x_start'))
	y_start = int(request.form.get('y_start'))
	x_end = int(request.form.get('x_end'))
	y_end = int(request.form.get('y_end'))
	img = user_profiles_uploadphoto.user_profiles_uploadphoto(token, img_url, x_start,
															 y_start, x_end, y_end)
	# Create a unique filename for the image to save it as and so it
	# can be referenced in the url
	filename = str(uuid.uuid1()) + ".jpg"
	# This adds the path to the file name and saves it in the upload folder
	full_filename = os.path.join(APP.config['UPLOAD_FOLDER'], filename)
	img.save(full_filename)

	# This adds the profile image url to the database
	port = request.host.split(':')[1]
	data.add_profile_image(token, filename, port)

	return dumps({})


# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# CHANNEL FUNCTIONS

@APP.route("/channel/invite", methods=["POST"])
def channel_invite_user():
	token = request.form.get("token")
	channel_id = int(request.form.get("channel_id"))
	user_id = int(request.form.get("u_id"))
	result = channel.channel_invite(token, channel_id, user_id)
	return dumps(result)

@APP.route("/channel/details", methods=["GET"])
def channel_get_details():
	token = request.args.get("token")
	channel_id = int(request.args.get("channel_id"))
	result = channel.channel_details(token, channel_id)
	return dumps(result)

@APP.route('/channel/messages', methods=['GET'])
def get_messages():
	token = request.args.get('token')
	channel_id = int(request.args.get('channel_id'))
	start = int(request.args.get('start'))
	result = channel.channel_messages(token, channel_id, start)
	return dumps(result)

@APP.route("/channel/leave", methods=["POST"])
def channel_user_leave():
	token = request.form.get("token")
	channel_id = int(request.form.get("channel_id"))
	result = channel.channel_leave(token, channel_id)
	return dumps(result)

@APP.route("/channel/join", methods=["POST"])
def channel_user_join():
	token = request.form.get("token")
	channel_id = int(request.form.get("channel_id"))
	result = channel.channel_join(token, channel_id)
	return dumps(result)

@APP.route("/channel/addowner", methods=["POST"])
def channel_add_owner():
	token = request.form.get("token")
	channel_id = int(request.form.get("channel_id"))
	user_id = int(request.form.get("u_id"))
	result = channel.channel_addowner(token, channel_id, user_id)
	return dumps(result)

@APP.route("/channel/removeowner", methods=["POST"])
def channel_remove_owner():
	token = request.form.get("token")
	channel_id = int(request.form.get("channel_id"))
	user_id = int(request.form.get("u_id"))
	result = channel.channel_removeowner(token, channel_id, user_id)
	return dumps(result)

@APP.route("/channels/list", methods=["GET"])
def channel_list_users_channels():
	token = request.args.get("token")
	result = channel.channel_list(token)
	return dumps(result)

@APP.route("/channels/listall", methods=["GET"])
def channel_list_all():
	token = request.args.get("token")
	result = channel.channel_listall(token)
	return dumps(result)

@APP.route("/channels/create", methods=["POST"])
def channel_add():
	token = request.form.get("token")
	name = request.form.get("name")
	is_public = request.form.get("is_public")
	result = channel.channel_create(token, name, is_public)
	return dumps(result)

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# MESSAGE FUNCTIONS

# MESSAGE SEND
@APP.route('/message/send', methods=['POST'])
def message_send():
	token = request.form.get('token')
	channel_id = int(request.form.get('channel_id'))
	message = request.form.get('message')

	message_id = message_profile.message_send(token, channel_id, message)
	return dumps(message_id)

# MESSAGE SEND LATER
@APP.route('/message/sendlater', methods=['POST'])
def message_sendlater():
	token = request.form.get('token')
	channel_id = int(request.form.get('channel_id'))
	message = request.form.get('message')
	time_sent = request.form.get('time_sent')
	# Convert time_sent to datetime
	time_sent = datetime.datetime.fromtimestamp(int(time_sent))
	message_id = message_profile.message_sendlater(
		token, channel_id, message, time_sent)

	return dumps(message_id)

# MESSAGE EDIT
@APP.route('/message/edit', methods=['PUT'])
def message_edit():
	token = request.form.get('token')
	message_id = int(request.form.get('message_id'))
	message = request.form.get('message')
	result = message_profile.message_edit(token, message_id, message)

	return dumps(result)

# MESSAGE REMOVE
@APP.route('/message/remove', methods=['DELETE'])
def message_remove():
	token = request.form.get('token')
	message_id = int(request.form.get('message_id'))
	result = message_profile.message_remove(token, message_id)

	return dumps(result)

# MESSAGE PIN
@APP.route('/message/pin', methods=['POST'])
def message_pin():
	token = request.form.get('token')
	message_id = int(request.form.get('message_id'))
	result = message_profile.message_pin(token, message_id)

	return dumps(result)

# MESSAGE UNPIN
@APP.route('/message/unpin', methods=['POST'])
def message_unpin():
	token = request.form.get('token')
	message_id = int(request.form.get('message_id'))
	result = message_profile.message_unpin(token, message_id)

	return dumps(result)

# MESSAGE REACT
@APP.route('/message/react', methods=['POST'])
def message_react():
	token = request.form.get('token')
	message_id = int(request.form.get('message_id'))
	react_id = int(request.form.get('react_id'))
	result = message_profile.message_react(token, message_id,react_id)
	return dumps(result)

# MESSAGE UNREACT
@APP.route('/message/unreact', methods=['POST'])
def message_unreact():
	token = request.form.get('token')
	message_id = int(request.form.get('message_id'))
	react_id = int(request.form.get('react_id'))

	result = message_profile.message_unreact(token, message_id, react_id)

	return dumps(result)
# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# ADMIN FUNCTION
@APP.route("/admin/userpermission/change", methods=["POST"])
def admin_user_permission_change():
	token = request.form.get("token")
	user_id = int(request.form.get("u_id"))
	permission_id = int(request.form.get("permission_id"))
	result = admin.admin_userpermission_change(token, user_id, permission_id)
	return dumps(result)

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# SEARCH FUNCTION

@APP.route("/search", methods=["GET"])
def search_message():
	token = request.args.get("token")
	query_str = request.args.get("query_str")
	result = search.search_messages(token, query_str)
	return dumps(result)

# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*
# Stand Up Function

@APP.route('/standup/active', methods=['GET'])
def standup_active_():
	token = request.args.get("token")
	channel_id = int(request.args.get("channel_id"))
	results = standup.standup_active(token,channel_id)
	return dumps(results)

@APP.route('/standup/start', methods=['POST'])
def standup_start_():
	token = request.form.get('token')
	channel_id = int(request.form.get('channel_id'))
	length = int(request.form.get('length'))
	results = standup.standup_start(token,channel_id,length)
	return dumps(results)

@APP.route('/standup/send', methods=['POST'])
def standup_send_():
	token = request.form.get('token')
	channel_id = int(request.form.get('channel_id'))
	message = request.form.get('message')
	results = standup.standup_send(token,channel_id,message)
	return dumps(results)
# -----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*-----*

@APP.route('/echo/get', methods=['GET'])
def echo1():
	""" Description of function """
	return dumps({
		'echo' : request.args.get('echo'),
	})

@APP.route('/echo/post', methods=['POST'])
def echo2():
	""" Description of function """
	return dumps({
		'echo' : request.form.get('echo'),
	})

if __name__ == '__main__':
	APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
