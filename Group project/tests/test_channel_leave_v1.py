import pytest
import json
import requests
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
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "password1", "name_first": "firstname1", "name_last": "lastname1"})
    token_dict = response1.json()
    return token_dict

@pytest.fixture
def token_dict2():
    #create user
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc2@gmail.com", "password": "password2", "name_first": "firstname2", "name_last": "lastname2"})
    token_dict = response1.json()
    return token_dict

@pytest.fixture
def token_dict3():
    #create user
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc3@gmail.com", "password": "password3", "name_first": "firstname3", "name_last": "lastname3"})
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

#if the channel_id is incorrect
def test_channel_leave_invalid_channel_id(setup, token_dict1, channel_id):
    token1 = token_dict1['token']
    #Test1 - channel is incorrect
    response1 = requests.post(config.url + 'channel/leave/v1', json = {"token": token1, "channel_id": channel_id + 1})
    assert response1.status_code == 400
    #Test2 - channel is empty
    response2 = requests.post(config.url + 'channel/leave/v1', json = {"token": token1, "channel_id": ""})
    assert response2.status_code == 400

#if the token is invalid
def test_channel_leave_invalid_token(setup, token_dict1, channel_id):
    token1 = token_dict1['token']
    #Test1 - wrong token
    response1 = requests.post(config.url + 'channel/leave/v1', json = {"token": token1 + "wrong", "channel_id": channel_id})
    assert response1.status_code == 403
    #Test2 - token is empty
    response2 = requests.post(config.url + 'channel/leave/v1', json = {"token": "", "channel_id": channel_id})
    assert response2.status_code == 403

def test_user_not_in_channel_leave(setup, token_dict1, token_dict2):
    token1 = token_dict1['token']
    token2 = token_dict2['token']
    response = requests.post(config.url + "channels/create/v2", json = {"token": token1, "name": "name", "is_public": True})
    ret = response.json()
    channel_id = ret['channel_id']
    response1 = requests.post(config.url + "channel/leave/v1", json = {"token": token2, "channel_id" : channel_id})
    assert response1.status_code == 403

def test_channel_leave_valid_owner_member(setup, token_dict1, token_dict2):
    token1 = token_dict1['token']
    token2 = token_dict2['token']
    auid2 = token_dict2['auth_user_id']
    response = requests.post(config.url + "channels/create/v2", json = {"token": token1, "name": "name", "is_public": True})
    ret = response.json()
    channel_id = ret['channel_id']
    requests.post(config.url + "channel/join/v2", json = {"token": token2, "channel_id" : channel_id})
    requests.post(config.url + "channel/leave/v1", json = {"token": token1, "channel_id" : channel_id})
    dict = {"token": token2, "channel_id": channel_id}
    response2 = requests.get(config.url + "channel/details/v2", params=dict)
    ret = response2.json()
    assert ret['owner_members'] == []
    assert ret['all_members'] == [{'u_id': auid2, 'email': 'abc2@gmail.com', 'name_first': 'firstname2', 'name_last': 'lastname2', 'handle_str': 'firstname2lastname2'}]

def test_channel_leave_valid_owner_member_join_invite(setup, token_dict1, token_dict2, token_dict3):
    token1 = token_dict1['token']
    token2 = token_dict2['token']
    auid2 = token_dict2['auth_user_id']
    auid3 = token_dict3['auth_user_id']
    response = requests.post(config.url + "channels/create/v2", json = {"token": token1, "name": "name", "is_public": True})
    ret = response.json()
    channel_id = ret['channel_id']
    requests.post(config.url + "channel/invite/v2", json = {"token" : token1, "channel_id" : channel_id, "u_id" : auid3})
    requests.post(config.url + "channel/join/v2", json = {"token": token2, "channel_id" : channel_id})
    requests.post(config.url + "channel/leave/v1", json = {"token": token1, "channel_id" : channel_id})
    dict = {'token' : token2, 'channel_id' : channel_id}
    response1 = requests.get(config.url + "channel/details/v2", params=dict)
    ret = response1.json()
    assert ret['owner_members'] == []
    assert ret['all_members'] == [{'u_id': auid3, 'email': 'abc3@gmail.com', 'name_first': 'firstname3', 'name_last': 'lastname3', 'handle_str': 'firstname3lastname3'}, {'u_id': auid2, 'email': 'abc2@gmail.com', 'name_first': 'firstname2', 'name_last': 'lastname2', 'handle_str': 'firstname2lastname2'}]

def test_channel_leave_valid_all_member(setup, token_dict1, token_dict2):
    token1 = token_dict1['token']
    token2 = token_dict2['token']
    auid1 = token_dict1['auth_user_id']
    response = requests.post(config.url + "channels/create/v2", json = {"token": token1, "name": "name", "is_public": True})
    ret = response.json()
    channel_id = ret['channel_id']
    requests.post(config.url + "channel/join/v2", json = {"token": token2, "channel_id" : channel_id})
    requests.post(config.url + "channel/leave/v1", json = {"token": token2, "channel_id" : channel_id})    
    dict = {'token' : token1, 'channel_id' : channel_id}
    response3 = requests.get(config.url + "channel/details/v2", params=dict)
    ret = response3.json()
    assert ret['owner_members'] == [{'u_id': auid1, 
                                       'email': 'abc@gmail.com', 
                                       'name_first': 'firstname1',
                                       'name_last': 'lastname1',
                                       'handle_str': 'firstname1lastname1'
                                       }]
    assert ret['all_members'] == [{'u_id': auid1, 
                                       'email': 'abc@gmail.com', 
                                       'name_first': 'firstname1',
                                       'name_last': 'lastname1',
                                       'handle_str': 'firstname1lastname1'
                                       }]

