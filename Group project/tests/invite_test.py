import pytest

from src.error import InputError, AccessError
from src.channel import channel_invite_v1
from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.other import clear_v1
from src.data_store import data_store

# If the channel_id is not valid
def test_valid_channel():
    clear_v1()
    user1_return = auth_register_v1('user1@gmail.com', 'Password123', 'Bob', 'Smith')
    user1_id = user1_return['auth_user_id']
    user2_return = auth_register_v1('user2@gmail.com', 'Password123', 'Mary', 'LOL')
    user2_id = user2_return['auth_user_id']
    channel = channels_create_v1(user1_id, 'channelname', True)
    channel_id = channel['channel_id']
    with pytest.raises(InputError):
        channel_invite_v1(user1_id, channel_id+1, user2_id)

# If the user being invited does not have a valid u_id
def test_valid_user():
    clear_v1()
    user1_return = auth_register_v1('user1@gmail.com', 'Password123', 'Bob', 'Smith')
    user1_id = user1_return['auth_user_id']
    user2_return = auth_register_v1('user2@gmail.com', 'Password123', 'Mary', 'LOL')
    user2_id = user2_return['auth_user_id']
    channel = channels_create_v1(user1_id, 'channelname', True)
    channel_id = channel['channel_id']
    with pytest.raises(InputError):
        channel_invite_v1(user1_id, channel_id, user1_id + user2_id + 1)

# If the user being invited is already in the channel
def test_valid_newmember():
    clear_v1()
    user1_return = auth_register_v1('user1@gmail.com', 'Password123', 'Bob', 'Smith')
    user1_id = user1_return['auth_user_id']
    channel = channels_create_v1(user1_id, 'channelname', True)
    channel_id = channel['channel_id']
    with pytest.raises(InputError):
        channel_invite_v1(user1_id, channel_id, user1_id)

# If the user doing the inviting (auth_user_id) has an invalid auth_user_id
def test_valid_invalid_authuser():
    clear_v1()
    user1_return = auth_register_v1('user1@gmail.com', 'Password123', 'Bob', 'Smith')
    user1_id = user1_return['auth_user_id']
    user2_return = auth_register_v1('user2@gmail.com', 'Password123', 'Mary', 'LOL')
    user2_id = user2_return['auth_user_id']
    channel = channels_create_v1(user1_id, 'channelname', True)
    channel_id = channel['channel_id']
    with pytest.raises(AccessError):
        channel_invite_v1(user1_id + user2_id + 1, channel_id, user2_id)

# Ensure the function returns correctly
def test_channel_invite_success():
    clear_v1()
    user1_return = auth_register_v1('user1@gmail.com', 'Password123', 'Bob', 'Smith')
    user1_id = user1_return['auth_user_id']
    user2_return = auth_register_v1('user2@gmail.com', 'Password123', 'Mary', 'LOL')
    user2_id = user2_return['auth_user_id']
    channel = channels_create_v1(user1_id, 'channelname', True)
    channel_id = channel['channel_id']
    assert channel_invite_v1(user1_id, channel_id, user2_id) == {}

# If the user doing the inviting (auth_user_id) is not in the channel
def test_channel_invite_authuser_not_in_channel():
    clear_v1()
    user1_return = auth_register_v1('user1@gmail.com', 'Password123', 'Bob', 'Smith')
    user1_id = user1_return['auth_user_id']
    user2_return = auth_register_v1('user2@gmail.com', 'Password123', 'Mary', 'LOL')
    user2_id = user2_return['auth_user_id']
    channel = channels_create_v1(user1_id, 'channelname', True)
    channel_id = channel['channel_id']
    with pytest.raises(AccessError):
        channel_invite_v1(user2_id, channel_id, user2_id)