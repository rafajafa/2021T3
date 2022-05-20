import requests
import pytest
from src import config

@pytest.fixture
def setup():
    requests.delete(config.url + 'clear/v1')

@pytest.fixture
def token():
    #create user1
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "password", "name_first": "raf", "name_last": "woo"})
    auid_dict = response1.json()
    token = auid_dict['token']
    return token

@pytest.fixture
def uid2():
    #create user2   
    response2 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc2@gmail.com", "password": "password", "name_first": "raf", "name_last": "woo"})
    auid_dict2 = response2.json()
    uid2 = auid_dict2['auth_user_id']
    return uid2

def test_invalid_uid(setup, token, uid2):
    # call user_profile with wrong uid
    wrong_uid = uid2 + 1
    dict = {'token' : token, 'u_id' : wrong_uid}
    response = requests.get(config.url + 'user/profile/v1', params=dict)    
    #input error
    assert (response.status_code == 400)

def test_invalid_token(setup, token, uid2):
    # call user_profile with wrong token
    wrong_token = token + "wrong"
    dict = {'token' : wrong_token, 'u_id' : uid2}
    response = requests.get(config.url + 'user/profile/v1', params=dict)
    # assess error
    assert (response.status_code == 403)

def test_valid_user_profile(setup, uid2):
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "password", "name_first": "name1", "name_last": "name2"})
    auid_dict = response1.json()
    token = auid_dict['token']
    dict = {'token' : token, 'u_id' : uid2}
    response = requests.get(config.url + 'user/profile/v1', params=dict)
    user_dict = response.json()
    user = user_dict['user']
    assert user == {'u_id': uid2, 'email': 'abc2@gmail.com', 'name_first' : 'raf', 'name_last' : 'woo', 'handle_str' : 'rafwoo'}
