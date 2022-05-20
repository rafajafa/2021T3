'''
import pytest
from src.error import AccessError, InputError
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.channel import channel_details_v1
from src.other import clear_v1
from src.auth import auth_register_v1

#Test to ensure that an AccessError is thrown if invalid auth_user_id is passed as an argument
def test_channel_create_invalid_uid():
        clear_v1()
        register_return = auth_register_v1('user1@gmail.com', 'Password123', 'Bob', 'Smith')
        auth_user_id = register_return['auth_user_id']
        with pytest.raises(AccessError):
                channels_create_v1(auth_user_id+1, 'channelname', True)

#Test to ensure that an InputError is thrown if name is too long or too short
def test_channels_invalid_name():
        clear_v1()
        register_return = auth_register_v1('user1@gmail.com', 'Password123', 'Bob', 'Smith')
        auth_user_id1 = register_return['auth_user_id']
        with pytest.raises(InputError):
                channels_create_v1(auth_user_id1, 'aaaaaaaaaaaaaaaaaaaaa', True)
                channels_create_v1(auth_user_id1, '', True)

#Test to ensure that channel_create would provide the correct channel_id
def test_channel_create_cid():
        clear_v1()
        register_return1 = auth_register_v1('user1@gmail.com', 'Password123', 'Bob', 'Smith')
        auth_user_id1 = register_return1['auth_user_id']
        create_return1 = channels_create_v1(auth_user_id1, 'channel_name', True)
        cid1 = create_return1['channel_id']
        list_all_return = channels_listall_v1(auth_user_id1)
        channels = list_all_return['channels']
        channel1 = channels[0]
        cid2 = channel1['channel_id']
        assert cid1 == cid2

#Test to ensure that if both channl name and auth_user_Id are both invalid throw an AccessError
def test_channel_create_invalid_uid_and_name():
        clear_v1()
        register_return = auth_register_v1('user1@gmail.com', 'Password123', 'Bob', 'Smith')
        auth_user_id = register_return['auth_user_id']
        with pytest.raises(AccessError):
                channels_create_v1(auth_user_id+1, 'aaaaaaaaaaaaaaaaaaaaa', True)

#Test to ensure that correct owner and all members are returned after channel is created
def test_channel_create_owner_and_members():
        clear_v1()
        register_return = auth_register_v1('user1@gmail.com', 'Password123', 'Bob', 'Smith')
        auth_user_id = register_return['auth_user_id']
        create_return = channels_create_v1(auth_user_id, 'channel1', True)
        channel_id1 = create_return['channel_id']
        details = channel_details_v1(auth_user_id, channel_id1)
        assert details['owner_members'] == [{'u_id': auth_user_id, 
                                         'email': 'user1@gmail.com', 
                                         'name_first': 'Bob',
                                         'name_last': 'Smith',
                                         'handle_str': 'bobsmith'
                                         }]

        assert details['all_members'] == [{'u_id': auth_user_id, 
                                         'email': 'user1@gmail.com', 
                                         'name_first': 'Bob',
                                         'name_last': 'Smith',
                                         'handle_str': 'bobsmith'
                                        }]

#Test to ensure that channel list is working correctly and returning the correct dictionary
def test_channel_list_valid():
        clear_v1()
        register_return = auth_register_v1('user1@gmail.com', 'Password123', 'Bob', 'Smith')
        auth_user_id1 = register_return['auth_user_id']
        channel_id_return = channels_create_v1(auth_user_id1, 'channel_1', True)
        channel_id1 = channel_id_return['channel_id']
        assert channels_list_v1(auth_user_id1) == {'channels': [{
               'channel_id' : channel_id1,
               'name' : 'channel_1' 
        }]}

#Test to ensure that an AccessError is thrown if an invalid auth_user_id is passed as argument
def test_channel_list_invalid_uid():
        clear_v1()
        register_return = auth_register_v1('user1@gmail.com', 'Password123', 'Bob', 'Smith')
        auth_user_id = register_return['auth_user_id']
        with pytest.raises(AccessError):
                channels_list_v1(auth_user_id+1)

'''