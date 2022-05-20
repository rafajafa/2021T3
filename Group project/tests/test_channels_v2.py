import requests
import pytest
import json
from json import dumps
from src import config
from src.other import clear_v1

@pytest.fixture
def setup():
    requests.delete(config.url + 'clear/v1')
    return dumps({}), 200

@pytest.fixture
def token():
    #create user1
    response = requests.post(config.url + 'auth/register/v2', json = {"email" : "user1@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    auid_dict = response.json()
    token = auid_dict['token']
    return token

@pytest.fixture
def token_dict():
    #create user1
    response = requests.post(config.url + 'auth/register/v2', json = {"email" : "user2@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    token_dict = response.json()
    return token_dict


def test_channel_create_invalid_token(setup, token):
    response = requests.post(config.url + 'channels/create/v2', json = {"token" : token + "wrong", "name" : "channel_name", "is_public" : True})
    assert response.status_code == 403

def test_channel_create_invalid_name(setup, token):
    response = requests.post(config.url + 'channels/create/v2', json = {"token" : token, "name" : "aaaaaaaaaaaaaaaaaaaaa", "is_public" : True})
    assert response.status_code == 400

def test_channel_create_cid(setup, token):
    response = requests.post(config.url + 'channels/create/v2', json = {"token" : token, "name" : "channel_name", "is_public" : True})
    channel_id_dict = response.json()
    cid1 = channel_id_dict['channel_id']
    list_response = requests.get(config.url + 'channels/listall/v2?token=' + token)
    list_all_dict = list_response.json()
    channels = list_all_dict['channels']
    channel1 = channels[0]
    cid2 = channel1['channel_id']
    assert cid1 == cid2

def test_channel_create_invalid_token_and_name(setup, token):
    response = requests.post(config.url + 'channels/create/v2', json = {"token" : token + "wrong", "name" : "aaaaaaaaaaaaaaaaaaaaa", "is_public" : True})
    assert response.status_code == 403

def test_channel_create_owner_and_members(setup, token_dict):
    token = token_dict['token']
    auth_user_id = token_dict['auth_user_id']
    response = requests.post(config.url + 'channels/create/v2', json = {"token" : token, "name" : "channel_name", "is_public" : True})
    channel_id_dict = response.json()
    channel_id = channel_id_dict['channel_id']

    dict = {'token' : token, 'channel_id' : channel_id}
    details_response = requests.get(config.url + 'channel/details/v2', params=dict)
    details_dict = details_response.json()
    assert details_dict['owner_members'] == [{'u_id': auth_user_id, 
                                         'email': 'user2@gmail.com', 
                                         'name_first': 'Bob',
                                         'name_last': 'Smith',
                                         'handle_str': 'bobsmith'
                                         }]
    assert details_dict['all_members'] == [{'u_id': auth_user_id, 
                                         'email': 'user2@gmail.com', 
                                         'name_first': 'Bob',
                                         'name_last': 'Smith',
                                         'handle_str': 'bobsmith'
                                        }]

def test_channel_list_invalid_token(setup, token):
    requests.post(config.url + 'channels/create/v2', json = {"token" : token, "name" : "channel_name", "is_public" : True})
    response = requests.get(config.url + 'channels/list/v2?token=' + token + "wrong")
    assert response.status_code == 403

def test_channel_list_valid(setup, token):
    response = requests.post(config.url + 'channels/create/v2', json = {"token" : token, "name" : "channel_name", "is_public" : True})
    channel_id_dict = response.json()
    channel_id = channel_id_dict['channel_id']
    list_response = requests.get(config.url + 'channels/list/v2?token=' + token)
    channel_list_dict = list_response.json()

    assert channel_list_dict == {'channels': [{
               'channel_id' : channel_id,
               'name' : 'channel_name' 
        }]}

def test_channel_list_two(setup, token):
    response = requests.post(config.url + 'channels/create/v2', json = {"token" : token, "name" : "channel_name", "is_public" : True})
    channel_id_dict = response.json()
    channel_id = channel_id_dict['channel_id']
    response2 = requests.post(config.url + 'channels/create/v2', json = {"token" : token, "name" : "channel_name2", "is_public" : True})
    channel_id_dict2 = response2.json()
    channel_id2 = channel_id_dict2['channel_id']
    list_response = requests.get(config.url + 'channels/list/v2?token=' + token)
    channel_list_dict = list_response.json()

    assert channel_list_dict == {'channels': [{
                'channel_id' : channel_id,
                'name' : 'channel_name' 
        },
                {'channel_id' : channel_id2,
                'name' : 'channel_name2'}]}

