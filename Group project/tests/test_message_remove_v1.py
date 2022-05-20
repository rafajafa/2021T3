import requests
import pytest
import json
import sys
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config

@pytest.fixture
def setup():
    requests.delete(config.url + 'clear/v1')

@pytest.fixture
def token_dict1():
	#create user
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc1@gmail.com", "password": "password1", "name_first": "firstname1", "name_last": "lastname1"})
    token_dict = response1.json()
    return token_dict

@pytest.fixture
def token_dict2():
	#create user
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc2@gmail.com", "password": "password2", "name_first": "firstname2", "name_last": "lastname2"})
    token_dict = response1.json()
    return token_dict
    
@pytest.fixture
def channel_id(token_dict1):
    token1 = token_dict1['token'] 
    #create channel 
    response2 = requests.post(config.url + 'channels/create/v2', json = {"token": token1, "name": "name", "is_public": True})
    channel_dict = response2.json()
    channel_id = channel_dict['channel_id']
    return channel_id

@pytest.fixture
def message_id(token_dict1,channel_id):
    token1 = token_dict1['token']
    response1 = requests.post(config.url + 'message/send/v1', json = {"token": token1, "channel_id": channel_id, "message": "massage"})
    message_dict = response1.json()
    message_id = message_dict['message_id']
    return message_id
	
@pytest.fixture
def dm_id(token_dict1):
    token1 = token_dict1['token']
    auid1 = token_dict1['auth_user_id']
    #create dm 
    response2 = requests.post(config.url + 'dm/create/v1', json = {"token": token1, "u_ids": [auid1]})
    dm_dict = response2.json()
    dm_id = dm_dict['dm_id']
    return dm_id
	  
#if message_id is wrong    
def test_invalid_messageid(setup, token_dict1, message_id):
    token1 = token_dict1['token']
    #Test1 - message_id is incorrect
    response1 = requests.delete(config.url + 'message/remove/v1', json = {"token": token1, "message_id": message_id + 1})
    assert response1.status_code == 400
    #Test2 - message_id is empty
    response2 = requests.delete(config.url + 'message/remove/v1', json = {"token": token1, "message_id": ""})
    assert response2.status_code == 400

#if the token is invalid
def test_token_invalid(setup, token_dict1, message_id):
    token1 = token_dict1['token']
    #Test1 - wrong token
    response1 = requests.delete(config.url + 'message/remove/v1', json = {"token": token1 + "wrong", "message_id": message_id})
    assert response1.status_code == 403
    #Test2 - token is empty
    response2 = requests.delete(config.url + 'message/remove/v1', json = {"token": "", "message_id": message_id})
    assert response2.status_code == 403
	
def test_message_remove_channelowner_valid(setup, token_dict1):
    token1 = token_dict1['token']
    response = requests.post(config.url + "channels/create/v2", json = {"token": token1, "name": "name", "is_public": True})
    ret = response.json()
    channel_id = ret['channel_id']
    response = requests.post(config.url + "message/send/v1", json = {"token": token1, "channel_id": channel_id, "message": "message"})
    ret = response.json()
    message_id = ret['message_id']
    requests.delete(config.url + "message/remove/v1", json = {"token": token1, "message_id": message_id})
    dict = {'token' : token1, 'channel_id' : channel_id, 'start' : 0}
    response1 = requests.get(config.url + "channel/messages/v2", params=dict)
    ret = response1.json()
    assert ret['messages'] == []
    
def test_message_remove_channeluser_valid(setup, token_dict1, token_dict2):
    token1 = token_dict1['token']
    token2 = token_dict2['token']
    response = requests.post(config.url + "channels/create/v2", json = {"token": token1, "name": "name", "is_public": True})
    ret = response.json()
    channel_id = ret['channel_id']
    requests.post(config.url + "channel/join/v2", json = {"token": token2, "channel_id": channel_id})
    response = requests.post(config.url + "message/send/v1", json = {"token": token2, "channel_id": channel_id, "message": "message"})
    ret = response.json()
    message_id = ret['message_id']
    requests.delete(config.url + "message/remove/v1", json = {"token": token2, "message_id": message_id})
    dict = {'token' : token1, 'channel_id' : channel_id, 'start' : 0}
    response1 = requests.get(config.url + "channel/messages/v2", params=dict)
    ret = response1.json()
    assert ret['messages'] == []
    
def test_message_remove_channel_notuser(setup, token_dict1, token_dict2):
    token1 = token_dict1['token']
    token2 = token_dict2['token']
    response = requests.post(config.url + "channels/create/v2", json = {"token": token1, "name": "name", "is_public": True})
    ret = response.json()
    channel_id = ret['channel_id']
    response1 = requests.post(config.url + "message/send/v1", json = {"token": token1, "channel_id": channel_id, "message": "message"})
    ret = response1.json()
    message_id = ret['message_id']
    response2 = requests.delete(config.url + "message/remove/v1", json = {"token": token2, "message_id": message_id})
    assert response2.status_code == 403
    
def test_message_remove_dm_notuser(setup, token_dict1, token_dict2):
    token1 = token_dict1['token']
    token2 = token_dict2['token']
    auid2 = token_dict2['auth_user_id']
    response = requests.post(config.url + "dm/create/v1", json = {"token": token1, "u_ids": [auid2]})
    ret = response.json()
    dm_id = ret['dm_id']
    response1 = requests.post(config.url + "message/senddm/v1", json = {"token": token1, "dm_id": dm_id, "message": "message"})
    ret = response1.json()
    message_id = ret['message_id']
    response2 = requests.delete(config.url + "message/remove/v1", json = {"token": token2, "message_id": message_id})
    assert response2.status_code == 403
    
def test_message_remove_dmowner_valid(setup, token_dict1, dm_id):
    token1 = token_dict1['token']
    response = requests.post(config.url + "message/senddm/v1", json = {"token": token1, "dm_id": dm_id, "message": "message"})
    ret = response.json()
    message_id = ret['message_id']
    requests.delete(config.url + "message/remove/v1", json = {"token": token1, "message_id": message_id})
    dict = {'token' : token1, 'dm_id' : dm_id, 'start' : 0}
    response1 = requests.get(config.url + "dm/messages/v1", params=dict)
    ret = response1.json()
    assert ret['messages'] == []
    
def test_message_remove_dmuser_valid(setup, token_dict1, token_dict2):
    token1 = token_dict1['token']
    token2 = token_dict2['token']
    auid2 = token_dict2['auth_user_id']
    response2 = requests.post(config.url + 'dm/create/v1', json = {"token": token1, "u_ids": [auid2]})
    dm_dict = response2.json()
    dm_id = dm_dict['dm_id']
    response = requests.post(config.url + "message/senddm/v1", json = {"token": token2, "dm_id": dm_id, "message": "message"})
    ret = response.json()
    message_id = ret['message_id']
    requests.delete(config.url + "message/remove/v1", json = {"token": token2, "message_id": message_id})
    dict = {'token' : token1, 'dm_id' : dm_id, 'start' : 0}
    response1 = requests.get(config.url + "dm/messages/v1", params=dict)
    ret = response1.json()
    assert ret['messages'] == []

def test_message_remove_permissions():
    requests.delete(config.url + 'clear/v1')

    response1 = requests.post(config.url + 'auth/register/v2', json={"email" : "user1@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    register_ret1 = response1.json()
    token1 = register_ret1['token']

    response2 = requests.post(config.url + 'auth/register/v2', json={"email" : "user2@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    register_ret2 = response2.json()
    token2 = register_ret2['token']
    auid2 = register_ret2['auth_user_id']
    
    channel_response = requests.post(config.url + 'channels/create/v2', json = {"token": token1, "name": "channel1", "is_public": False})
    channel_return = channel_response.json()
    cid = channel_return['channel_id']

    requests.post(config.url + 'channel/invite/v2', json = {"token": token1, "channel_id": cid,"u_id": auid2})

    send_response = requests.post(config.url + 'message/send/v1', json = {"token": token1, "channel_id": cid, "message": "Hello"})
    send_ret = send_response.json()
    msg_id = send_ret['message_id']

    remove_response1 = requests.delete(config.url + 'message/remove/v1', json = {"token": token2, "message_id": msg_id})
    assert remove_response1.status_code == 403

    requests.post(config.url + 'channel/addowner/v1', json = {"token": token1, "channel_id": cid, "u_id": auid2})

    remove_response2 = requests.delete(config.url + 'message/remove/v1', json = {"token": token2, "message_id": msg_id})
    assert remove_response2.status_code == 200