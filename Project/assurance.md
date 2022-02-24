# Marking criteria for assurance

* Demonstration of an understanding of the need for software verification and validation
* Development of appropriate acceptance criteria based on user stories and requirements.
* Demonstration of appropriate tool usage for assurance (code coverage, linting, etc.)

# Assurance

## Software Verification and Validation
Verification- are we building the product right?
* Checked against product specifications and implemented the functional and non-functional requirement specifications
* Built against user acceptance criteria and implementing logic based on backend data handling.
* Several examples are listed below

Validation- Are we building the right product?
* Checks that the product satisfies the intended use
* We worked to the user requirements set out in user stories. This included the user acceptance criteria in our task board on Gitlab that we wrote up in iteration 1.
* Since the user requirements were derived directly from the interview with the client, it further validated the purpose of our product.
* In the process of developing the software, we considered many design questions to see whether they satisfied the requirements set at the beginning by the user interview.
Through this, we've developed a product that's followed the client specifications every step of the way.
Not only this, our tests were written from the specs given to us and the software was written in a test driven development process.

### Tokens
Authorisation
* Thoroughly considered with the use of JWT token verification after logging in.
* Testing whether the user calling the function is authorised to have access to the action. e.g.:
    * Process to authenticate tokens and add them to active tokens list when a user logs in
    * This token is then passed around to all functions which verfiy whether the token is active before allowing the user to take an action
    * It also checks whether the user is in the channel they are attempting to access or whether they have certain permissions
    * Token is then invalidated after the user logs out so someone with the same token cannot have access to the app

Authentication
* User is authenticated when they log in with the correct email and password by providing them with an active token
* There were also checks through the program to ensure they are authenticated to access any

### Slackr admins and channel ownership

Assuming all slackr admins are automatically members and owners of all channels. They can not be removed from ownership from any channel.

### Promoting/demoting admins and channels

We had a couple of options for how this would work but we ended up deciding that when an admin is demoted, they would be stripped of all owner permissions from every channel, but they will remain as members in every channel. Our other option was to remove admins from every channel when they have their admin rights stripped from them but we thought that it would make more sense to have to remove admins from channels they were not previously a part of than having to add them back to the channels they were previously a part of.

### Search

The search function only returns messages from channels that the user is a part of.

### channels_listall

Assuming listall to a regular user lists all public channels that are available to join.

### Messages
* By utilising the *user acceptance criteria* and the specifications provided we were able to produce functions that manipulated a data structure that house all the variables the messages would interact and modify with.

* We used a mixture of *integration and system testing* in our message tests to provide a solution that would ensure we fulfilled our *verification criteria*
* In terms of integration testing we had tests that were aimed at potential faults in the code and logic
* While in terms of *system testing* we had tests that were aimed at certain attributes which were detailed out in the specs given.
* To ensure our solution for messages was valid we split the logic down to simple *goals* to ensure we meet the *overall objective* of the given message function

## Appropriate User Acceptance Criteria

All in GitLab

## Appropriate Tool Usage For Assurance

Important Note: Our tests only have the following coverage scores if we run them separately.
This is because we wrote our tests to interact with a global dictionary which doesn't get reset in between tests.

# Pytest Coverage

admin_userpermission_change - 92%
search_messages - 100%
channel - 94%
message_profile - 82%
message_send_later - 100%
user_profile_test - 100%
auth_test - 100%

# Test Coverage
In our test driven development cycle, we completed our tests prior to creating the functions, allowing us to clearly determine what we expect each function to do and achieve. Throughout our development we also referred to our tests and coded to meet their functional and nonfunctional specifications. We used **unit tests** for all our functions to test that they worked individually or with minimal interaction with other functions. We also used **integration tests** when we had functions which relied on other functions. This way of testing allowed us to see that the whole program works together cohesively. We also had a minimal API which improved our integration testing as it allowed us to interact with our data in a cleaner way. We also performed minimal **system testing** with the server.py and running it with the frontend to check that certain functions worked the way we expected them to. Doing this allowed us to pick up on many bugs to fix and make the program work more efficiently. Since we do not have an actual audience to do **user acceptance testing** with, we created user acceptance criteria to follow whilst creating our code.

# Pylint

channel, admin_userpermission_change, search_messages

Pylint scores are quite low for the above as there are a lot of inconsistent tabs/spaces for some reason. Even after fixing these pylint is still giving a low score.

user_profile.py = 8.57

# Data structure

Spreadsheet describing the data structure is here: https://docs.google.com/spreadsheets/d/1cn26fZbQmMGPNzKBVRqX8JKPfXTQIhDw6TRjlD8mrLQ/edit?usp=sharing