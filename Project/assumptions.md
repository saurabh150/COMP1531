# Overall
Assuming 3 users are already registered on database for the purposes of testing:

##Owner

* e-mail: “owner@email.com”
* password: “OwnerPassword”
* uId: 333333
* token: “OwnerToken”

##Admin
* e-mail: admin@email.com
* password: AdminPassword
* uId: 222222
* token: “AdminToken”

##User
* e-mail: user@email.com
* password: UserPassword
* uId: 111111
* token: “UserToken”

## User Profile
`user_profile(token, uId) (Jia Min)`

* Assume that given wrong token id, program throws a value error
* An invalid uId passed into the function could be either unauthorised or nonexistent

`user_profile_setname(token, name_first, name_last) (Jia Min)`

* Length of name cannot be 0
* Certain characters cannot be in the name. E.g. `@#$%^&*()`

`user_profile_setemail(token, email) (Jia Min)`

* Backend will go to database to check whether the email has been used
* Will use REGEX to check whether email entered is valid
* May send an email confirmation

`user_profile_sethandle(token, handleStr) (Jia Min`

* Certain characters cannot be in the handle
* Length of name cannot be 0
* Handle doesn’t have to be unique

## Channels
`channel_invite(token, channel_id, u_id) (Jason)`

* valid channelId = 1
* invalid channelId = 0 (assuming admin is not part of valid channel referred to by 0)
* valid uId = 1
* invalid uId = 0
* Assuming `channel_details()` will be implemented and used to test correctness later
* Assuming `channels_create()` will be implemented and used to test correctness later

`channel_details(token, channel_id) (Jia Min)`

* All members includes owner members
* There will be also a parameter for admin members

`channel_messages(token, channel_id, start) (Jia Min)`

* In the future, is unread will show who has read the message
* Time created will never be in the past

`channel_leave(token, channel_id) (Jason)`

* valid channelId = 1
* invalid nonexistent channel's channelId = 0
* Assuming `channel_details()` will be implemented and used to test correctness later
* Assuming `channels_create()` will be implemented and used to test correctness later

`channel_join(token, channel_id) (Jason)`

* valid channelId = 1
* nonexistent channelId = 0
* Assuming userToken represents a user that does not have access to private channel 1
* Assuming `channel_details()` will be implemented and used to test correctness later
* Assuming `channels_create()` will be implemented and used to test correctness later

`channel_addowner(token, channel_id, u_id) (Jason)`

* channelId = 1 is an existing channel
* channelId = 0 is a nonexistent channel
* uId = 111111 is a regular user of channel with channel ID 1
* uId = 222222 is a user that is already the owner of the channel with channel ID 1
* uId = 0 does not exist
* Assuming `"OwnerToken"` is token belonging to owner of the slackr/channel
* Assuming `channel_details()` will be implemented and used to test correctness later
* Assuming `channels_create()` will be implemented and used to test correctness later

`channel_removeowner(token, channel_id, u_id) (Jason)`

* channelId = 1 is an existing channel
* channelId = 0 is a nonexistent channel
* uId = 111111 is a regular user of channel with channel ID 1
* uId = 333333 is a user that is already the owner of the channel with channel ID 1
* uId = 0 does not exist
* Assuming `"OwnerToken"` is token belonging to owner of the slackr/channel
* Assuming `channel_details()` will be implemented and used to test correctness later
* Assuming `channels_create()` will be implemented and used to test correctness later

`channels_create(token, name, is_public) (Saurabh)`

* Users are created in each function individually as all tests require to be run independently of other tests.
* After creating a few lists, used `channels_listall()` to test if it was created as that function shows all the channels created.
* The current stub functions will cause most tests to fail, but with the actual functions the tests will check the function from every aspect.
* The `channels_listall()` function has no errors.
* The flag variables are used to check every channel individually with its channel id.
* Asserted `true == false`, so it breaks if that line runs (it’s not supposed to if function is correct).

`channels_list(token) (Saurabh)`

* The token is a string, and as it is created within the backend, it isn’t wrong.
* The helper functions used here to test the authenticity of the return data all work with no errors themselves.
* The users and channels created in each test are meant for testing in its respective test functions only, to independently test the function from each aspect

`channels_listall(token) (Saurabh)`

* The token is a string, and as it is created within the backend, it isn’t wrong.
* The helper functions used here to test the authenticity of the return data all work with no errors themselves.
* The users and channels created in each test are meant for testing in its respective test functions only, to independently test the function from each aspect


## Messages

`message_remove(token, messageId) (Eddy)`

* Good messageId = 1
* Bad messageId = 0

`message_send(token, channelId, messageId) (Eddy)`

* Valid token = “correct”
* ChannelId = 1

`message_send_later(token, channelId, messageId) (Eddy)`

* Have access to messages
* Have a function that compares the current computer tick time, date to the time given by the message function to thus send the message (Use `import dateTime` and use the iso format for the clock) valid channel iD must be between 0 and 10

`message_edit(token, messageId, message) (Eddy)`

* Assume token = authorized
* Token messageID = 1
* Message associated with messageID = 1 is "hello how are you going today?"
* Assumption that I will later be able to check that a user has access to certain messages
* I will be able to view the message later to confirm the change with message_view
* Assumption I will later be able to test authorization token

`message_pin(token, messageId) (Eddy)`

* pin status: 1 = pinned, 0 = unpinned
* Authorized token = `"authorized token1"` and has admin level privileges
* Valid messageId is greater than or equal to 1
* To be part of the channel token must have the integer 1 in it's string at the end like so `"authorized token1"`
* Later be able to use a channel function to show if pin was successful

`message_unpin(token, messageId) (Eddy)`

* pinned = 1
* unPinned = 0
* Assumption I am modifying only one message, (messageID = 1)
* Assumption that I will be able to later view if the messageId is unpinned

`message_react(token, messageId, reactId) (Eddy)`

* messageIDs have to be greater than 0 to be valid
* any messageID less than or equal to 0 is not valid
* valid reactIDs must be greater than 0, anything equal to or below 0 is invalid
* Later able to use a channel function to tell me if the react(multiple and/or different) was successfully attached to the message

`message_unreact(token, messageId, reactId) (Eddy)`

* messageIDs have to be greater than 0 to be valid
* any messageID less than or equal to 0 is not valid
* valid reactIDs must be greater than 0, anything equal to or below 0 is invalid
* Later able to use a channel function to tell me if the react(multiple and/or different) was successfully attached to the message

## Standups

`standup_start(token, channel_id) (Jason)`

* Assuming owner has permission to start standup time
* Assuming user does not have permission to start standup time/not a member of channel 1
* existing channelId = 1
* nonexistent channelId = 0
* Assuming `channels_create()` will be implemented and used to test correctness later
* Assuming `channel_messages()` will be implemented and used to test correctness later

`standup_send(token, channel_id, message) (Jason)`

* Assuming that ownerToken is a token belonging to a user that is a member of channel 1
* Assuming that userToken is a token belonging to a user that is not a member of channel 1
* existing channelId = 1
* nonexistent channelId = 0
* Assuming `channels_create()` will be implemented and used to test correctness later
* For the purposes of this test, assuming temporary global variable `standup_stopped` indicates whether the standup time has been stopped

## Settings

`admin_userpermission_change(token, u_id, permission_id) (Jason)`

* Assuming userToken is the token of a user that is not admin/owner
* valid uId = 1 that refers to a valid user with token userToken
* invalid uId = 0 that does not refer to a valid user
* valid permissionId = 1 that refers to the admin value permission level
* invalid permissionId = 0 that does not refer to a value permission
* Assuming there is already a channel and message with ID 1 to pin for testing administrator permissions
* Assuming `channel_messages()` will be implemented and used to test correctness later

`search(token, query_str) (Jason)`

* Assuming that empty string token = "" is an unauthorised token
* Assuming return is a list of dictionaries representing messages
* Assuming regular user is authorised to search

## Authentication

`auth_login(email, password) (Saurabh)`

* These tests are meant to be run on the actual function, hence might fail in iteration 1.
* As the input will be from the website, if the user enters nothing into the fields for email and password then it will assume that the input was email: “” and password: “” which are invalid email and password.
* Each user is registered within a function itself, it’s repetitive but helps to test the function from every aspect.
* Assuming that all helper functions used have no errors themselves.

`auth_logout(token) (Saurabh)`

* Channels_list function has no error and takes care of invalid token.
* Registration of each user in the test function itself is repetitive but supports the purpose of testing the logout function from different aspects.
* After logout, the previous token isn’t valid anymore - not just the fact that the function loses the variables value in memory.

`auth_register(email, password, name_first, name_list) (Sauarbh)`

* When a user registers, an email is sent with a confirmation to the user’s email which he/she used to create an account. This will have to be checked manually.
* An invalid email is a string without the character `“@”` and at least one `“.”`
* The invalid password string is yet unknown, so it’s just used as `“WrongPasswordType”`, will change this in iteration2.
* `User_profile` works with no errors. 

`auth_passwordreset_reset(reset_code, new_password) (Saurabh)`

* The reset code will have to be manually added to the functions as the code is sent to the email. 
* For now assuming a correct `reset_code` will be `“CorrectCode”` and correct `new_password` will be `“CorrectPassword”`
* Assuming that the wrong `reset_code` will be `“inCorrectCode”` and wrong password will be `“inCorrectPassword”`

`auth_passwordreset_request(email) (Saurabh)`

* Assuming that if an email is incorrect it doesn’t throw any exceptions.
* To check if the code is received, will have to test manually.
* Even if the function works or doesn’t it returns {} only.
