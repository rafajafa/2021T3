import pytest

from src.channels import channels_create_v1
from src.channel import channel_messages_v1
from src.auth import auth_login_v1, auth_register_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.data_store import data_store    

# test if channel id is wrong
def test_not_valid_channel_id():
    clear_v1()
    register_return = auth_register_v1('user1@gmail.com', 'user1password', 'user1', 'user1')
    auth_user_id1 = register_return['auth_user_id']
    channels_create_v1(auth_user_id1,'channel_name', True)
    register_return = auth_login_v1('user1@gmail.com', 'user1password',)
    auth_user_id1 = register_return['auth_user_id']
    create_return = channels_create_v1(auth_user_id1, 'channel_name', True)
    cid = create_return['channel_id']
    with pytest.raises(InputError):
        channel_messages_v1(auth_user_id1, cid + 1, 0)

# test if start is too large
def test_start_greater_total_msg():
    clear_v1()
    register_return = auth_register_v1('user1@gmail.com', 'user1password', 'user1', 'user1')
    auth_user_id1 = register_return['auth_user_id']
    channels_create_v1(auth_user_id1,'channel_name', True)
    register_return = auth_register_v1('user2@gmail.com', 'user2password', 'user2', 'user2')
    auth_user_id1 = register_return['auth_user_id']
    create_return = channels_create_v1(auth_user_id1,'channel_name', True) 
    cid = create_return['channel_id']
    with pytest.raises(InputError):
        channel_messages_v1(auth_user_id1, cid, 10)

# test if user id is wrong
def test_not_valid_user_id():
    clear_v1()
    register_return = auth_register_v1('user1@gmail.com', 'user1password', 'user1', 'user1')
    auth_user_id1 = register_return['auth_user_id']
    channels_create_v1(auth_user_id1,'channel_name', True)
    register_return = auth_register_v1('user2@gmail.com', 'user2password', 'user2', 'user2')
    auth_user_id2 = register_return['auth_user_id']
    create_return = channels_create_v1(auth_user_id1,'channel_name', True) 
    cid = create_return['channel_id']
    with pytest.raises(AccessError):
        channel_messages_v1(auth_user_id2, cid, 0)

# test for valid msg
def test_valid_message():
    clear_v1()
    register_return = auth_register_v1('user1@gmail.com', 'user1password', 'user1', 'user1')
    auth_user_id1 = register_return['auth_user_id']
    create_return = channels_create_v1(auth_user_id1,'channel_name', True) 
    cid = create_return['channel_id']
    assert channel_messages_v1(auth_user_id1, cid, 0) == {'messages' : [], 'start' : 0, 'end' : -1}

# test for non exist user
def test_not_valid_user_id_2():
    clear_v1()
    wrong_user_id = -1
    register_return = auth_register_v1('user1@gmail.com', 'user1password', 'user1', 'user1')
    auth_user_id1 = register_return['auth_user_id']
    create_return = channels_create_v1(auth_user_id1,'channel_name', True) 
    cid = create_return['channel_id']
    with pytest.raises(AccessError):
        channel_messages_v1(wrong_user_id, cid, 0)