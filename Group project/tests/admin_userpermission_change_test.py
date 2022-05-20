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

@pytest.fixture
def uid3():
    #create user2   
    response3 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc3@gmail.com", "password": "password", "name_first": "raf", "name_last": "woo"})
    auid_dict3 = response3.json()
    uid3 = auid_dict3['auth_user_id']
    return uid3

def test_invalid_uid(setup, token, uid2):
    response = requests.post(config.url + 'admin/userpermission/change/v1', json = {"token" : token, "u_id" : uid2+1, "permission_id" : 1})
    assert response.status_code == 400

def test_invalid_token(setup, token, uid2):
    wrong_token = token + 'wrong'
    response = requests.post(config.url + 'admin/userpermission/change/v1', json = {"token" : wrong_token, "u_id" : uid2, "permission_id" : 1})
    assert response.status_code == 403

def test_invalid_permission_id(setup, token, uid2, uid3):
    response = requests.post(config.url + 'admin/userpermission/change/v1', json = {"token" : token, "u_id" : uid2, "permission_id" : 3})
    assert response.status_code == 400

def test_invalid_demote_if_only_one_owner(setup):
    #create user1
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email" : "abc@gmail.com", "password" : "12345678", "name_first" : "raf", "name_last" : "woo"})
    auid_dict = response1.json()
    token = auid_dict['token']
    uid = auid_dict['auth_user_id']
    # demote the only golbal user to user
    response = requests.post(config.url + 'admin/userpermission/change/v1', json = {"token" : token, "u_id" : uid, "permission_id" : 2})
    assert response.status_code == 400

def test_invalid_user_not_owner(setup, token, uid3):
    #create user2  
    response2 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc2@gmail.com", "password": "password", "name_first": "raf", "name_last": "woo"})
    auid_dict2 = response2.json()
    token2 = auid_dict2['token']
    # user is not global user
    response = requests.post(config.url + 'admin/userpermission/change/v1', json = {"token" : token2, "u_id" : uid3, "permission_id" :  1})
    assert response.status_code == 403
    

def test_valid_promotedemote(setup):
    #create user1
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email" : "abc@gmail.com", "password" : "12345678", "name_first" : "raf", "name_last" : "woo"})
    auid_dict = response1.json()
    token = auid_dict['token']
    uid = auid_dict['auth_user_id']
    #create user2
    response2 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc2@gmail.com", "password": "password", "name_first": "raf", "name_last": "woo"})   
    auid_dict2 = response2.json()
    token2 = auid_dict2['token']
    uid2 = auid_dict2['auth_user_id']
    #promote user2 to global
    admin_response = requests.post(config.url + 'admin/userpermission/change/v1', json = {"token" : token, "u_id" : uid2, "permission_id" : 1})
    assert admin_response.status_code == 200
    #demote user1 to user 
    admin_response1 = requests.post(config.url + 'admin/userpermission/change/v1', json = {"token" : token2, "u_id" : uid, "permission_id" : 2})
    assert admin_response1.status_code == 200
