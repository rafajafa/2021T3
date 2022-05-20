'''
import pytest
from src.channel import channel_details_v1
from src.channel import channel_join_v1
from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.error import InputError
from src.error import AccessError
from src.other import clear_v1

#auth_user_id invalid
def test_channel_join_v1():
	clear_v1()
	register_return = auth_register_v1('abc@gmail.com', 'password', 'first_name', 'last_name')
	auth_user_id = register_return['auth_user_id']
	create_return = channels_create_v1(auth_user_id, 'channel1', True)
	channel_id = create_return['channel_id']
	with pytest.raises(AccessError):
		channel_join_v1(auth_user_id+1,channel_id)

#channel_id invalid
def test_channel_join_v2():
	clear_v1()
	register_return1 = auth_register_v1('abc@gmail.com', 'password', 'first_name', 'last_name')
	auth_user_id1 = register_return1['auth_user_id']
	register_return2 = auth_register_v1('efg@gmail.com', 'password', 'first_name', 'last_name')
	auth_user_id2 = register_return2['auth_user_id']
	create_return = channels_create_v1(auth_user_id1, 'channel1', True)
	channel_id = create_return['channel_id']
	with pytest.raises(InputError):
		channel_join_v1(auth_user_id2,channel_id+1)
 
#user already in the channel   
def test_channel_join_already():
    clear_v1()
    register_return = auth_register_v1('abc@gmail.com', 'password', 'first_name', 'last_name')
    auth_user_id = register_return['auth_user_id']
    create_return = channels_create_v1(auth_user_id, 'channel1', True)
    channel_id = create_return['channel_id']
    with pytest.raises(InputError):
	    channel_join_v1(auth_user_id,channel_id)

#global member join the private channel
def test_channel_join_private():
	clear_v1()
	register_return1 = auth_register_v1('abc@gmail.com', 'password', 'first_name', 'last_name')
	auth_user_id1 = register_return1['auth_user_id']
	register_return2 = auth_register_v1('efg@gmail.com', 'password', 'first_name', 'last_name')
	auth_user_id2 = register_return2['auth_user_id']
	create_return = channels_create_v1(auth_user_id1, 'channel1', False)
	channel_id = create_return['channel_id']
	with pytest.raises(AccessError):
	    channel_join_v1(auth_user_id2,channel_id)
		
#global owner join private channel
def test_channel_join_global():
	clear_v1()
	register_return1 = auth_register_v1('abc@gmail.com', 'password', 'first_name', 'last_name')
	auth_user_id1 = register_return1['auth_user_id']
	register_return2 = auth_register_v1('efg@gmail.com', 'password', 'first_name', 'last_name')
	auth_user_id2 = register_return2['auth_user_id']
	create_return = channels_create_v1(auth_user_id2, 'channel1', False)
	channel_id = create_return['channel_id']
	channel_join_v1(auth_user_id1,channel_id)
	details = channel_details_v1(auth_user_id1,channel_id)
	assert details['owner_members'] == [{'u_id': auth_user_id2, 
                                         'email': 'efg@gmail.com', 
                                         'name_first': 'first_name',
                                         'name_last': 'last_name',
                                         'handle_str': 'firstnamelastname0'
                                         }]
	assert details['all_members'] == [{'u_id': auth_user_id2, 
                                       'email': 'efg@gmail.com', 
                                       'name_first': 'first_name',
                                       'name_last': 'last_name',
                                       'handle_str': 'firstnamelastname0'
				       },
					{'u_id': auth_user_id1, 
                                       'email': 'abc@gmail.com', 
                                       'name_first': 'first_name',
                                       'name_last': 'last_name',
                                       'handle_str': 'firstnamelastname'
                                       }]
	
'''