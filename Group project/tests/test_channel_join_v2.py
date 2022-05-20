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
def channel_id(token_dict1):
    token1 = token_dict1['token']
    #create channel 
    response2 = requests.post(config.url + 'channels/create/v2', json = {"token": token1, "name": "name", "is_public": True})
    channel_dict = response2.json()
    channel_id = channel_dict['channel_id']
    return channel_id

@pytest.fixture
def token_dict1():
    #create user
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "password", "name_first": "firstname", "name_last": "lastname"})
    token_dict = response1.json()
    return token_dict

@pytest.fixture
def token_dict2():
    #create user
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc2@gmail.com", "password": "password", "name_first": "firstname", "name_last": "lastname"})
    token_dict = response1.json()
    return token_dict

#if the channel_id is incorrect
def test_channeljoin_invalid_channel_id(setup, token_dict1, channel_id):
    token1 = token_dict1['token']
    #Test1 - channel is incorrect
    response1 = requests.post(config.url + 'channel/join/v2', json = {"token": token1, "channel_id": channel_id + 1})
    assert response1.status_code == 400

#if the token is invalid
def test_channeljoin_invalid_token(setup, token_dict1, channel_id):
    token1 = token_dict1['token']
    #Test1 - wrong token
    response1 = requests.post(config.url + 'channel/join/v2', json = {"token": token1 + "wrong", "channel_id": channel_id})
    assert response1.status_code == 403
    #Test2 - token is empty
    response2 = requests.post(config.url + 'channel/join/v2', json = {"token": "", "channel_id": channel_id})
    assert response2.status_code == 403

def test_user_already_in_channel(setup, token_dict1, token_dict2):
    token1 = token_dict1['token']
    token2 = token_dict2['token']
    response = requests.post(config.url + "channels/create/v2", json = {"token": token1, "name": "name", "is_public": True})
    ret = response.json()
    channel_id = ret['channel_id']
    join_response1 = requests.post(config.url + "channel/join/v2", json = {"token": token1, "channel_id" : channel_id})
    assert join_response1.status_code == 400
    requests.post(config.url + "channel/join/v2", json = {"token": token2, "channel_id" : channel_id})
    join_response2 = requests.post(config.url + "channel/join/v2", json = {"token": token2, "channel_id" : channel_id})
    assert join_response2.status_code == 400

def test_join_channel_private(setup, token_dict1, token_dict2):
    token1 = token_dict1['token']
    token2 = token_dict2['token']
    response = requests.post(config.url + "channels/create/v2", json = {"token": token1, "name": "name", "is_public": False})
    ret = response.json()
    channel_id = ret['channel_id']
    response = requests.post(config.url + "channel/join/v2", json = {"token": token2, "channel_id" : channel_id})
    assert response.status_code == 403
    
def test_globaluser_join_channel_private(setup, token_dict1, token_dict2):
    token1 = token_dict1['token']
    token2 = token_dict2['token']
    auth_user_id1 = token_dict1['auth_user_id']
    auth_user_id2 = token_dict2['auth_user_id']
    response = requests.post(config.url + "channels/create/v2", json = {"token": token1, "name": "name", "is_public": True})
    ret = response.json()
    channel_id = ret['channel_id']
    response = requests.post(config.url + "channel/join/v2", json = {"token": token2, "channel_id" : channel_id})
    dict = {'token' : token2, 'channel_id' : channel_id}
    response1 = requests.get(config.url + "channel/details/v2", params=dict)
    ret = response1.json()
    assert ret['owner_members'] == [{'u_id': auth_user_id1, 
                                       'email': 'abc@gmail.com', 
                                       'name_first': 'firstname',
                                       'name_last': 'lastname',
                                       'handle_str': 'firstnamelastname'
                                       }]
    assert ret['all_members'] == [{'u_id': auth_user_id1, 
                                       'email': 'abc@gmail.com', 
                                       'name_first': 'firstname',
                                       'name_last': 'lastname',
                                       'handle_str': 'firstnamelastname'
                                       },
                                    {'u_id': auth_user_id2, 
                                       'email': 'abc2@gmail.com', 
                                       'name_first': 'firstname',
                                       'name_last': 'lastname',
                                       'handle_str': 'firstnamelastname0'
                                        }]
    
def test_user_join_private_channel_private(setup, token_dict1):
    token1 = token_dict1['token']
    auth_user_id1 = token_dict1['auth_user_id']
    response = requests.post(config.url + "channels/create/v2", json = {"token": token1, "name": "name", "is_public": False})
    ret = response.json()
    channel_id = ret['channel_id']
    requests.post(config.url + "channel/leave/v2", json = {"token": token1, "channel_id" : channel_id})
    response = requests.post(config.url + "channel/join/v2", json = {"token": token1, "channel_id" : channel_id})
    dict = {'token' : token1, 'channel_id' : channel_id}
    response1 = requests.get(config.url + "channel/details/v2", params=dict)
    ret = response1.json()
    assert ret['owner_members'] == [{'u_id': auth_user_id1, 
                                       'email': 'abc@gmail.com', 
                                       'name_first': 'firstname',
                                       'name_last': 'lastname',
                                       'handle_str': 'firstnamelastname'
                                       }]
    assert ret['all_members'] == [{'u_id': auth_user_id1, 
                                       'email': 'abc@gmail.com', 
                                       'name_first': 'firstname',
                                       'name_last': 'lastname',
                                       'handle_str': 'firstnamelastname'
                                       }]