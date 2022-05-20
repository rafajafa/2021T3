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
def dm_id(token_dict1):
    token1 = token_dict1['token']
    auid1 = token_dict1['auth_user_id']
    #create dm 
    response2 = requests.post(config.url + 'dm/create/v1', json = {"token": token1, "u_ids": [auid1]})
    dm_dict = response2.json()
    dm_id = dm_dict['dm_id']
    return dm_id

#id the dm_id is wrong
def test_dmid_invalid_dmid(setup, token_dict1, dm_id):
    token1 = token_dict1['token']
    #Test1 - dm_id is incorrect
    response1 = requests.post(config.url + 'dm/leave/v1', json = {"token": token1, "dm_id": dm_id + 1})
    assert response1.status_code == 400
    response1 = requests.post(config.url + 'dm/leave/v1', json = {"token": token1, "dm_id": ""})
    assert response1.status_code == 400

#if the token is invalid
def test_token_invalid(setup, token_dict1, dm_id):
    token1 = token_dict1['token']
    #Test1 - wrong token
    response1 = requests.post(config.url + 'dm/leave/v1', json = {"token": token1 + "wrong", "dm_id": dm_id})
    assert response1.status_code == 403
    #Test2 - token is empty
    response2 = requests.post(config.url + 'dm/leave/v1', json = {"token": "", "dm_id": dm_id})
    assert response2.status_code == 403

def test_not_dm_member_leave(setup, token_dict1, token_dict2):
    token1 = token_dict1['token']
    token2 = token_dict2['token']
    auid1 = token_dict1['auth_user_id']
    response = requests.post(config.url + "dm/create/v1", json = {"token": token1, "u_ids": [auid1]})
    ret = response.json()
    dm_id = ret['dm_id']
    response = requests.post(config.url + "dm/leave/v1", json = {"token": token2, "dm_id": dm_id})
    assert response.status_code == 403
    
def test_dm_leave(setup, token_dict1, token_dict2):
    token1 = token_dict1['token']
    token2 = token_dict2['token']
    auid2 = token_dict2['auth_user_id']
    response = requests.post(config.url + "dm/create/v1", json = {"token": token1, "u_ids": [auid2]})
    ret = response.json()
    dm_id = ret['dm_id']
    requests.post(config.url + "dm/leave/v1", json = {"token": token1, "dm_id": dm_id})
    dict = {'token': token2, 'dm_id' : dm_id}
    response1 = requests.get(config.url + "dm/details/v1", params=dict)
    ret = response1.json()
    assert ret['members'] == [{'u_id': auid2, 'email': 'abc2@gmail.com', 'name_first': 'firstname2', 'name_last': 'lastname2', 'handle_str': 'firstname2lastname2'}]
    
def test_dmowner__leave(setup, token_dict1, token_dict2):
    token1 = token_dict1['token']
    token2 = token_dict2['token']
    auid1 = token_dict1['auth_user_id']
    auid2 = token_dict2['auth_user_id']
    response = requests.post(config.url + "dm/create/v1", json = {"token": token1, "u_ids": [auid2]})
    ret = response.json()
    dm_id = ret['dm_id']
    requests.post(config.url + "dm/leave/v1", json = {"token": token2, "dm_id": dm_id})
    dict = {'token': token1, 'dm_id' : dm_id}
    response1 = requests.get(config.url + "dm/details/v1", params=dict)
    ret = response1.json()
    assert ret['members'] == [{'u_id': auid1, 'email': 'abc1@gmail.com', 'name_first': 'firstname1', 'name_last': 'lastname1', 'handle_str': 'firstname1lastname1'}]

