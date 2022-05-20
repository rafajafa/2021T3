'''
import pytest

from src.channels import channels_create_v1, channels_listall_v1
from src.auth import auth_login_v1, auth_register_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.data_store import data_store

# test for user2 checking all channels user1 create
def test_otheruser_listall_channel():
    clear_v1()
    register_return = auth_register_v1('user1@gmail.com', 'user1password', 'user1', 'user1')
    auth_user_id1 = register_return['auth_user_id']
    register_return = auth_register_v1('user2@gmail.com', 'user2password', 'user2', 'user2')
    auth_user_id2 = register_return['auth_user_id']
    channels_return = channels_create_v1(auth_user_id1, "channel1", True)
    channel_id1 = channels_return['channel_id']
    channels_return = channels_create_v1(auth_user_id1, "channel2", False)
    channel_id2 = channels_return['channel_id']
    channels_return = channels_listall_v1(auth_user_id2)
    channels = channels_return['channels']
    assert((channels == [{'channel_id' : channel_id1, 'name' : 'channel1'}, {'channel_id' : channel_id2, 'name' : 'channel2'}]))

# test for user1 checking all channels user1 create
def test_listall_channels():
    clear_v1()
    register_return = auth_register_v1('user1@gmail.com', 'user1password', 'user1', 'user1')
    auth_user_id1 = register_return['auth_user_id']
    channels_return = channels_create_v1(auth_user_id1, "channel1", True)
    channel_id1 = channels_return['channel_id']
    channels_return = channels_create_v1(auth_user_id1, "channel2", False)
    channel_id2 = channels_return['channel_id']
    channels_return = channels_listall_v1(auth_user_id1)
    channels = channels_return['channels']
    assert((channels == [{'channel_id' : channel_id1, 'name' : 'channel1'}, {'channel_id' : channel_id2, 'name' : 'channel2'}]))


# test for non exist user
def test_not_valid_user_id():
    clear_v1()
    wrong_user_id = -1
    with pytest.raises(AccessError):
        channels_listall_v1(wrong_user_id)
'''


