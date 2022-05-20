import requests
import pytest
import json
from json import dumps
from src import config
from src.other import clear_v1

@pytest.fixture
def setup():
    requests.delete(config.url + 'clear/v1')

@pytest.fixture
def token():
    #create user
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "password", "name_first": "Ja", "name_last": "mes"})
    auid_dict = response1.json()
    token = auid_dict['token']
    return token

@pytest.fixture
def token2():
    #create user
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc2@gmail.com", "password": "password", "name_first": "Ja", "name_last": "mes"})
    auid_dict = response1.json()
    token2 = auid_dict['token']
    return token2

@pytest.fixture
def channel_id(token):
    #create channel 
    response2 = requests.post(config.url + 'channels/create/v2', json = {"token": token, "name": "name", "is_public": True})
    channel_dict = response2.json()
    channel_id = channel_dict['channel_id']
    return channel_id

@pytest.fixture
def channel_id2(token2):
    #create channel 
    response3 = requests.post(config.url + 'channels/create/v2', json = {"token": token2, "name": "name", "is_public": True})
    channel_dict = response3.json()
    channel_id = channel_dict['channel_id']
    return channel_id

@pytest.fixture
def token_dict1():
    #create user
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc3@gmail.com", "password": "password", "name_first": "firstname", "name_last": "lastname"})
    token_dict = response1.json()
    return token_dict

@pytest.fixture
def token_dict2():
    #create user
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc4@gmail.com", "password": "password", "name_first": "firstname", "name_last": "lastname"})
    token_dict = response1.json()
    return token_dict

def test_channel_details_invalid_channel(setup, token, channel_id, token2, channel_id2):
    dict = {'token' : token, 'channel_id' : channel_id + 100}
    response = requests.get(config.url + 'channel/details/v2', params=dict)
    assert response.status_code == 400

def test_channel_details_invalid_token(setup, token, channel_id, token2):
    dict = {'token' : token + 'wrong', 'channel_id' : channel_id}
    response = requests.get(config.url + 'channel/details/v2', params=dict)
    assert response.status_code == 403
    dict = {'token' : token2, 'channel_id' : channel_id}
    response = requests.get(config.url + 'channel/details/v2', params=dict)
    assert response.status_code == 403

def test_channel_details_valid_invite(setup, token_dict1, token_dict2):
    token1 = token_dict1['token']
    uid1 = token_dict1['auth_user_id']
    uid2 = token_dict2['auth_user_id']
    response = requests.post(config.url + 'channels/create/v2', json = {"token": token1, "name": "name", "is_public": True})
    channel_dict = response.json()
    channel_id = channel_dict['channel_id']
    requests.post(config.url + "channel/invite/v2", json = {"token" : token1, "channel_id" : channel_id, "u_id" : uid2})
    
    dict = {'token' : token1, 'channel_id' : channel_id}
    response = requests.get(config.url + 'channel/details/v2', params=dict)
    details = response.json()
    print(details)
    assert details['name'] == 'name'
    assert details['is_public'] == True
    assert details['owner_members'] == [{'u_id': uid1, 
                                         'email': 'abc3@gmail.com', 
                                         'name_first': 'firstname',
                                         'name_last': 'lastname',
                                         'handle_str': 'firstnamelastname'
                                         }]
    assert details['all_members'] == [{'u_id': uid1, 
                                         'email': 'abc3@gmail.com', 
                                         'name_first': 'firstname',
                                         'name_last': 'lastname',
                                         'handle_str': 'firstnamelastname'
                                         }, 
                                      {'u_id': uid2, 
                                       'email': 'abc4@gmail.com', 
                                       'name_first': 'firstname',
                                       'name_last': 'lastname',
                                       'handle_str': 'firstnamelastname0'
                                       }]

def test_channel_details_success(setup, token_dict1):
    token1 = token_dict1['token']
    uid1 = token_dict1['auth_user_id']
    response = requests.post(config.url + 'channels/create/v2', json = {"token": token1, "name": "name", "is_public": True})
    channel_dict = response.json()
    channel_id = channel_dict['channel_id']
    dict = {'token' : token1, 'channel_id' : channel_id}
    response = requests.get(config.url + 'channel/details/v2', params=dict)
    ret = response.json()
    assert ret['name'] == 'name'
    assert ret['owner_members'][0]['u_id'] == uid1
    assert ret['all_members'][0]['u_id'] == uid1
    assert ret['is_public'] == True
