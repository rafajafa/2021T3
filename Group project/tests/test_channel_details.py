'''
import pytest
from src.channel import channel_details_v1
from src.channel import channel_invite_v1
from src.channel import channel_join_v1
from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.error import InputError
from src.error import AccessError
from src.other import clear_v1

# Test to ensure that the returned details are correct
def test_channel_details_return_details_correct():
    clear_v1()
    register_return = auth_register_v1('abc@gmail.com', 'password', 'first_name', 'last_name')
    auth_user_id = register_return['auth_user_id']
    create_return = channels_create_v1(auth_user_id, 'channel1', True)
    channel_id = create_return['channel_id']
    details = channel_details_v1(auth_user_id, channel_id)
    assert details['name'] == 'channel1'
    assert details['is_public'] == True
    assert details['owner_members'] == [{'u_id': auth_user_id, 
                                         'email': 'abc@gmail.com', 
                                         'name_first': 'first_name',
                                         'name_last': 'last_name',
                                         'handle_str': 'firstnamelastname'
                                         }]
    assert details['all_members'] == [{'u_id': auth_user_id, 
                                       'email': 'abc@gmail.com', 
                                       'name_first': 'first_name',
                                       'name_last': 'last_name',
                                       'handle_str': 'firstnamelastname'
                                       }]

# Test to ensure that an InputError is thrown when an invalid channel_id is passed as an argument
def test_channel_details_invalid_channel():
    clear_v1()
    register_return = auth_register_v1('abc@gmail.com', 'password', 'first_name', 'last_name')
    auth_user_id = register_return['auth_user_id']
    create_return = channels_create_v1(auth_user_id, 'channel1', True)
    channel_id = create_return['channel_id']
    with pytest.raises(InputError):
        channel_details_v1(auth_user_id, channel_id + 1)

# Test to ensure that a non-member should not have access to the channel details
def test_channel_details_invalid_access():
    clear_v1()
    register_return1 = auth_register_v1('abc@gmail.com', 'password1', 'first_name1', 'last_name1')
    auth_user_id1 = register_return1['auth_user_id']
    register_return2 = auth_register_v1('efg@gmail.com', 'password2', 'first_name2', 'last_name2')
    auth_user_id2 = register_return2['auth_user_id']
    create_return = channels_create_v1(auth_user_id1, 'channel1', False)
    channel_id1 = create_return['channel_id']
    with pytest.raises(AccessError):
        channel_details_v1(auth_user_id2, channel_id1)

# Test to ensure that an InputError if an invalid channel is passed as an argument
def test_channel_details_invalid_channel_2():
    clear_v1()
    register_return1 = auth_register_v1('abc@gmail.com', 'password1', 'first_name1', 'last_name1')
    auth_user_id1 = register_return1['auth_user_id']
    register_return2 = auth_register_v1('efg@gmail.com', 'password2', 'first_name2', 'last_name2')
    auth_user_id2 = register_return2['auth_user_id']
    create_return = channels_create_v1(auth_user_id1, 'channel1', False)
    channel_id1 = create_return['channel_id']
    with pytest.raises(InputError):
        channel_details_v1(auth_user_id2, channel_id1 + 1)

# Test to ensure that an AccessError is thrown when an invalid auth_user_id is passed as an argument
def test_channel_details_invalid_user():
    clear_v1()
    register_return = auth_register_v1('abc@gmail.com', 'password', 'first_name', 'last_name')
    auth_user_id = register_return['auth_user_id']
    create_return = channels_create_v1(auth_user_id, 'channel1', True)
    channel_id = create_return['channel_id']
    with pytest.raises(AccessError):
        channel_details_v1(auth_user_id + 1, channel_id)


# Test to ensure a user can view details after joining a channel
def test_channel_details_access_after_join():
    clear_v1()
    register_return1 = auth_register_v1('abc@gmail.com', 'password1', 'first_name1', 'last_name1')
    auth_user_id1 = register_return1['auth_user_id']
    register_return2 = auth_register_v1('efg@gmail.com', 'password2', 'first_name2', 'last_name2')
    auth_user_id2 = register_return2['auth_user_id']
    create_return = channels_create_v1(auth_user_id1, 'channel1', True)
    channel_id1 = create_return['channel_id']
    channel_join_v1(auth_user_id2, channel_id1)
    details = channel_details_v1(auth_user_id1, channel_id1)
    assert details['name'] == 'channel1'
    assert details['is_public'] == True
    assert details['owner_members'] == [{'u_id': auth_user_id1, 
                                         'email': 'abc@gmail.com', 
                                         'name_first': 'first_name1',
                                         'name_last': 'last_name1',
                                         'handle_str': 'firstname1lastname1'
                                         }]
    assert details['all_members'] == [{'u_id': auth_user_id1, 
                                       'email': 'abc@gmail.com', 
                                       'name_first': 'first_name1',
                                       'name_last': 'last_name1',
                                       'handle_str': 'firstname1lastname1'
                                       }, 
                                      {'u_id': auth_user_id2, 
                                       'email': 'efg@gmail.com', 
                                       'name_first': 'first_name2',
                                       'name_last': 'last_name2',
                                       'handle_str': 'firstname2lastname2'
                                         }]


# Ensure that a user can view the correct details of the channel after beinginvited to it
def test_channel_details_access_after_invite():
    clear_v1()
    register_return1 = auth_register_v1('abc@gmail.com', 'password1', 'first_name1', 'last_name1')
    auth_user_id1 = register_return1['auth_user_id']
    register_return2 = auth_register_v1('efg@gmail.com', 'password2', 'first_name2', 'last_name2')
    auth_user_id2 = register_return2['auth_user_id']
    create_return = channels_create_v1(auth_user_id1, 'channel1', False)
    channel_id1 = create_return['channel_id']
    channel_invite_v1(auth_user_id1, channel_id1, auth_user_id2)
    details = channel_details_v1(auth_user_id1, channel_id1)
    assert details['name'] == 'channel1'
    assert details['is_public'] == False
    assert details['owner_members'] == [{'u_id': auth_user_id1, 
                                         'email': 'abc@gmail.com', 
                                         'name_first': 'first_name1',
                                         'name_last': 'last_name1',
                                         'handle_str': 'firstname1lastname1'
                                         }]
    assert details['all_members'] == [{'u_id': auth_user_id1, 
                                       'email': 'abc@gmail.com', 
                                       'name_first': 'first_name1',
                                       'name_last': 'last_name1',
                                       'handle_str': 'firstname1lastname1'
                                       }, 
                                      {'u_id': auth_user_id2, 
                                       'email': 'efg@gmail.com', 
                                       'name_first': 'first_name2',
                                       'name_last': 'last_name2',
                                       'handle_str': 'firstname2lastname2'
                                       }]

def test_details_invalid_channel():
    clear_v1()
    user1_return = auth_register_v1('user1@gmail.com', 'Password123', 'Bob', 'Smith')
    user1_id = user1_return['auth_user_id']
    channel = channels_create_v1(user1_id, 'channelname', True)
    channel_id = channel['channel_id']
    with pytest.raises(InputError):
        channel_details_v1(user1_id, channel_id+1)

def test_details_invalid_authuser():
    clear_v1()
    user1_return = auth_register_v1('user1@gmail.com', 'Password123', 'Bob', 'Smith')
    user1_id = user1_return['auth_user_id']
    user2_return = auth_register_v1('user2@gmail.com', 'Password123', 'Mary', 'LOL')
    user2_id = user2_return['auth_user_id']
    channel = channels_create_v1(user1_id, 'channelname', True)
    channel_id = channel['channel_id']
    with pytest.raises(AccessError):
        channel_details_v1(user2_id, channel_id)

def test_details_success():
    clear_v1()
    user1_return = auth_register_v1('user1@gmail.com', 'Password123', 'Bob', 'Smith')
    user1_id = user1_return['auth_user_id']
    channel = channels_create_v1(user1_id, 'channelname', True)
    channel_id = channel['channel_id']
    result = channel_details_v1(user1_id, channel_id)
    assert result['name'] == 'channelname'
    assert result['owner_members'][0]['u_id'] == user1_id
    assert result['all_members'][0]['u_id'] == user1_id
    assert result['is_public'] == True

'''