import requests
import pytest
from src import config
from src.other import clear_v1
from src.helpers import generate_jwt

@pytest.fixture
def setup():
    requests.delete(config.url + 'clear/v1')

@pytest.fixture
def token():
    #create user1
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

# test if channel id is wrong
def test_not_valid_channel_id_v2(setup, token):
    # create channel1
    response3 = requests.post(config.url + 'channels/create/v2', json = {"token" : token, "name" : "channel1", "is_public" : True})
    channel_id_dict = response3.json()
    channel_id = channel_id_dict['channel_id']
    # call channel_messages_v2
    dict = {'token' : token, 'channel_id' : channel_id+1, 'start' : 0}
    response3 = requests.get(config.url + 'channel/messages/v2', params=dict)
    assert (response3.status_code == 400)

# test if start is too large
def test_start_greater_total_msg_v2(setup, token):
    # create channel1
    response3 = requests.post(config.url + 'channels/create/v2', json = {"token" : token, "name" : "channel1", "is_public" : True})
    channel_id_dict = response3.json()
    channel_id = channel_id_dict['channel_id']
    # call channel_messages_v2 
    dict = {'token' : token, 'channel_id' : channel_id, 'start' : 10}
    response3 = requests.get(config.url + 'channel/messages/v2', params=dict)
    assert (response3.status_code == 400)

# test if user id is wrong
def test_not_valid_user_id(setup, token, token2):
    # create channel1
    response3 = requests.post(config.url + 'channels/create/v2', json = {"token" : token, "name" : "channel1", "is_public" : True})
    channel_id_dict = response3.json()
    channel_id = channel_id_dict['channel_id']
    # call channel_messages_v2
    dict = {'token' : token2, 'channel_id' : channel_id, 'start' : 0}
    response = requests.get(config.url + 'channel/messages/v2', params=dict)
    assert (response.status_code == 403)

# test for valid msg
def test_valid_message_v2(setup, token):
    # create channel1
    response3 = requests.post(config.url + 'channels/create/v2', json = {"token" : token, "name" : "channel1", "is_public" : True})
    channel_id_dict = response3.json()
    channel_id = channel_id_dict['channel_id']
    # call channel_messages_v2
    dict = {'token' : token, 'channel_id' : channel_id, 'start' : 0}
    response3 = requests.get(config.url + 'channel/messages/v2', params=dict)
    messages_dict = response3.json()
    assert (messages_dict == {'messages' : [], 'start' : 0, 'end' : -1})

def test_valid_message_v2_2(setup, token):
    # create channel1
    response3 = requests.post(config.url + 'channels/create/v2', json = {"token" : token, "name" : "channel1", "is_public" : True})
    channel_id_dict = response3.json()
    channel_id = channel_id_dict['channel_id']
    for i in range(0, 51):
        requests.post(config.url + 'message/send/v1', json = {"token": token, "channel_id": channel_id, "message": "msg"})
        i = i+1
    # call channel_messages_v2
    dict = {'token' : token, 'channel_id' : channel_id, 'start' : 0}
    response3 = requests.get(config.url + 'channel/messages/v2', params=dict)
    messages_dict = response3.json()
    start = messages_dict['start']
    end = messages_dict['end']
    assert (start == 0 and end == 50)

# test for non exist user
def test_not_valid_user_id_v2_2(setup, token):
    # create channel1
    response3 = requests.post(config.url + 'channels/create/v2', json = {"token" : token, "name" : "channel1", "is_public" : True})
    channel_id_dict = response3.json()
    channel_id = channel_id_dict['channel_id']

    wrong_user_token = generate_jwt(-1, -1)
    dict = {'token' : wrong_user_token, 'channel_id' : channel_id, 'start' : 0}
    response3 = requests.get(config.url + 'channel/messages/v2', params=dict)
    assert (response3.status_code == 403)
