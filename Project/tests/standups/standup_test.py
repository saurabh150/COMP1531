import datetime
from datetime import timezone
from functions.auth import auth_login, auth_register
from functions.exceptions import AccessError, ValueError
from functions.standup import standup_start, standup_send, standup_active
from functions.channel import channel_create, channel_join
from functions.data import reset_data, get_standup_messages, get_channels, get_messages

def test_activate_standup():
    reset_data()
    user1 = auth_register('user1@email.com', 'password', 'User1','Rob')
    #user2 = auth_register('user2@email.com', 'password', 'User2','Rob')

    channel1 = channel_create(user1['token'],'Channel 1', True)
    standup1 = standup_start(user1['token'], channel1['channel_id'],0.1)

    standup_check = standup_active(user1['token'],channel1['channel_id'])
    assert standup_check['is_active'] ==  True
    assert standup_check['time_finish'] ==  standup1['time_finish']

# Checks if the user who started the standup is from who the final msg is sent
# Checks if the correct msg is sent
# Checks if message was sent after the standup actually ended
def test_send_msg():
    reset_data()
    user1 = auth_register('user1@email.com', 'password', 'User1','Rob')
    user2 = auth_register('user2@email.com', 'password', 'User2','Rob')

    # As user 1 is owner, assuming user already in the channel
    channel1 = channel_create(user2['token'],'Channel 1', True)
    standup1 = standup_start(user2['token'], channel1['channel_id'],0.1)
    standup_check = standup_active(user1['token'],channel1['channel_id'])
    assert standup_check['is_active'] ==  True
    assert standup_check['time_finish'] ==  standup1['time_finish']

    i = 0
    while i < 2:
        standup_send(user1['token'],channel1['channel_id'], f'Counter is at {i}')
        i += 1

    # Buffer to wait for standup to end
    flag = True
    while flag:
        active_check = standup_active(user1['token'], channel1['channel_id'])
        flag = (active_check['is_active'] == True)

    msg_struct = get_messages()[0]
    msg_to_compare = 'user1rob: Counter is at 0\nuser1rob: Counter is at 1\n'
    assert msg_struct['u_id'] == user2['u_id']
    assert msg_struct['time_created'] >= standup_check['time_finish']
    assert msg_struct['message'] == msg_to_compare

def test_msg_sent_after_standup_end():
    reset_data()
    user1 = auth_register('user1@email.com', 'password', 'User1','Rob')

    channel1 = channel_create(user1['token'],'Channel 1', True)
    standup1 = standup_start(user1['token'], channel1['channel_id'],0.1)
    standup_check = standup_active(user1['token'],channel1['channel_id'])
    assert standup_check['is_active'] ==  True
    assert standup_check['time_finish'] ==  standup1['time_finish']

    # Buffer to wait for standup to end
    flag = True
    while flag:
        active_check = standup_active(user1['token'], channel1['channel_id'])
        flag = (active_check['is_active'] == True)

    try:
        standup_send(user1['token'],channel1['channel_id'],'LOL SAD LYF')
        assert True is False
    except ValueError:
        print ('Passed')

# Try to start a standup after it is active already
def test_standup_start_during_active_standup():
    reset_data()
    user1 = auth_register('user1@email.com', 'password', 'User1','Rob')

    channel1 = channel_create(user1['token'],'Channel 1', True)
    standup_start(user1['token'], channel1['channel_id'],0.1)

    try:
        standup_start(user1['token'], channel1['channel_id'],0.1)
        assert True is False
    except ValueError:
        print("Passed")

# Try to start standup when not in the channel
def test_not_in_channel_standup_start():
    reset_data()
    user1 = auth_register('user1@email.com', 'password', 'User1','Rob')
    user2 = auth_register('user2@email.com', 'password', 'User2','Rob')

    channel1 = channel_create(user1['token'],'Channel 1', True)

    try:
        standup_start(user2['token'], channel1['channel_id'],0.1)
        assert True is False
    except AccessError:
        print("Passed")

# Test trying to send message with more than 1000 chars.
def test_more_than_1000_char():
    reset_data()
    user1 = auth_register('user1@email.com', 'password', 'User1','Rob')
    #user2 = auth_register('user2@email.com', 'password', 'User2','Rob')

    channel1 = channel_create(user1['token'],'Channel 1', True)
    standup_start(user1['token'], channel1['channel_id'],0.1)
    x = "Hi" * 1000
    try:
        standup_send(user1['token'],channel1['channel_id'], x)
        assert True is False
    except ValueError:
        print("Passed")
