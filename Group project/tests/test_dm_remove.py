import requests
import pytest
from src import config
from src.other import clear_v1

@pytest.fixture
def setup():
    requests.delete(config.url + 'clear/v1')

@pytest.fixture
def token():
    #create user1
    response = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "password", "name_first": "raf", "name_last": "woo"})
    #response = requests.post(config.url + 'auth/login/v2', json = {"email": "abc@gmail.com", "password": "password"})
    auid_dict = response.json()
    token = auid_dict['token']
    return token

@pytest.fixture
def token2():
    #create user2
    response2 = requests.post(config.url + 'auth/register/v2', json={"email" : "user2@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    register_ret2 = response2.json()
    token2 = register_ret2['token']
    return token2

@pytest.fixture
def uid2():
    #create user2   
    response2 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc2@gmail.com", "password": "password", "name_first": "raf", "name_last": "woo"})
    auid_dict2 = response2.json()
    uid2 = auid_dict2['auth_user_id']
    return uid2

@pytest.fixture
def dm_create(token, uid2):
    dm_response = requests.post(config.url + 'dm/create/v1', json = {"token" : token, "u_ids" : [uid2]})
    print(token)
    dmid_dict = dm_response.json()
    dm_create_obj = {}
    dm_create_obj['dm_id'] = dmid_dict['dm_id']
    dm_create_obj['owner_token'] = token
    return dm_create_obj

#wrong token, access error
def test_invalid_dmid(setup, dm_create):
    response = requests.delete(config.url + "dm/remove/v1", json = {"token" : dm_create["owner_token"], "dm_id" : dm_create['dm_id'] + 1})
    assert response.status_code == 400
    
def test_success_remove(setup, dm_create, token2):
    response = requests.delete(config.url + "dm/remove/v1", json = {"token" : dm_create["owner_token"], "dm_id" : dm_create["dm_id"]})
    assert response.status_code == 200

def test_non_owner_delete_1(setup, dm_create, token2):
    response = requests.delete(config.url + "dm/remove/v1", json = {"token" : token2, "dm_id" : dm_create["dm_id"]})
    assert response.status_code == 403