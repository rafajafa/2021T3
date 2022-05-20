import pytest
import json
import requests
from src import config
from src.other import clear_v1

@pytest.fixture
def setup():
    requests.delete(config.url + 'clear/v1')

@pytest.fixture
def token():
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "password", "name_first": "first_name", "name_last": "last_name"})
    auid_dict = response1.json()
    token = auid_dict['token']
    return token

@pytest.fixture
def token2():
    response2 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc2@gmail.com", "password": "password", "name_first": "raf", "name_last": "woo"})
    auid_dict2 = response2.json()
    token2 = auid_dict2['token']
    return token2


# test for user2 checking all channels user1 create
def test_otheruser_listall_channel_v2(setup, token, token2):

    # create channel1
    response3 = requests.post(config.url + 'channels/create/v2', json = {"token" : token, "name" : "channel1", "is_public" : True})
    channel_id_dict = response3.json()
    channel_id1 = channel_id_dict['channel_id']
    # create channel2
    response4 = requests.post(config.url + 'channels/create/v2', json = {"token" : token, "name" : "channel2", "is_public" : True})
    channel_id_dict2 = response4.json()
    channel_id2 = channel_id_dict2['channel_id']
    
    # call listall v2
    channels = requests.get(config.url + 'channels/listall/v2?token='+ token2)
    channels_dict = channels.json()
    channels = channels_dict['channels']
    # assert the returned list of dict is correct
    assert((channels == [{'channel_id' : channel_id1, 'name' : 'channel1'}, {'channel_id' : channel_id2, 'name' : 'channel2'}]))

# test for user1 checking all channels user1 create
def test_listall_channels_v2(setup, token):

    # create channel1
    response3 = requests.post(config.url + 'channels/create/v2', json = {"token" : token, "name" : "channel1", "is_public" : True})
    channel_id_dict = response3.json()
    channel_id1 = channel_id_dict['channel_id']
    # create channel2
    response4 = requests.post(config.url + 'channels/create/v2', json = {"token" : token, "name" : "channel2", "is_public" : True})
    channel_id_dict2 = response4.json()
    channel_id2 = channel_id_dict2['channel_id']
    
    # call listall v2
    channels = requests.get(config.url + 'channels/listall/v2?token=' + token)
    channels_dict = channels.json()
    channels = channels_dict['channels']
    # assert the returned list of dict is correct
    assert((channels == [{'channel_id' : channel_id1, 'name' : 'channel1'}, {'channel_id' : channel_id2, 'name' : 'channel2'}]))

# test for non exist user
def test_not_valid_user_id_v2():
    wrong_user_token = '-1'
    response = requests.get(config.url + 'channels/listall/v2?token='+ wrong_user_token)
    #access error
    assert(response.status_code == 403)

