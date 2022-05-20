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

@pytest.fixture
def uid3():
    #create user2   
    response3 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc3@gmail.com", "password": "password", "name_first": "raf", "name_last": "woo"})
    auid_dict3 = response3.json()
    uid3 = auid_dict3['auth_user_id']
    return uid3

def test_not_valid_uid_in_uids(setup):
    #create user1
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "password", "name_first": "raf", "name_last": "woo"})
    auid_dict = response1.json()
    token = auid_dict['token']
    wrong_uid = auid_dict['auth_user_id'] + 1
    #call dm/create/v1
    response = requests.post(config.url + 'dm/create/v1', json = {"token" : token, "u_ids" : [wrong_uid]})
    #return input error
    assert (response.status_code == 400)


def test_valid_dmid(setup, token, uid2, uid3):
    #call dm/create/v1
    dm_response = requests.post(config.url + 'dm/create/v1', json = {"token" : token, "u_ids" : [uid2]})
    #call dm/create/v1
    dm_response2 = requests.post(config.url + 'dm/create/v1', json = {"token" : token, "u_ids" : [uid3]})
    dmid_dict = dm_response.json()
    dmid2_dict = dm_response2.json()
    dmid = dmid_dict['dm_id'] 
    dmid2 = dmid2_dict['dm_id'] 

    requests.post(config.url + 'dm/create/v1', json = {"token" : token, "u_ids" : [uid2]})
    assert (dmid == 1 and dmid2 == 2)

def test_not_valid_token(setup, token, uid2):
    wrong_token = token + "wrong"
    #call dm/create/v1
    response = requests.post(config.url + 'dm/create/v1', json = {"token" : wrong_token, "u_ids" : [uid2]})
    #return access error
    assert (response.status_code == 403)

def test_name_sorted_by_handle(setup, token):
    #create user2 call rafwoo
    response2 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc2@gmail.com", "password": "password", "name_first": "raf", "name_last": "woo"})
    auid_dict2 = response2.json()
    uid2 = auid_dict2['auth_user_id']
    #create user3, call abcwoo
    response3 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc3@gmail.com", "password": "password", "name_first": "def", "name_last": "woo"})
    auid_dict3 = response3.json()
    uid3 = auid_dict3['auth_user_id']

    #call dm/create/v1
    dm_response = requests.post(config.url + 'dm/create/v1', json = {"token" : token, "u_ids" : [uid2, uid3]})
    dmid_dict = dm_response.json()
    dmid = dmid_dict['dm_id']
    dict = {'token': token, 'dm_id' : dmid}
    dm_detail_dict = requests.get(config.url + 'dm/details/v1', params=dict)
    dm_detail = dm_detail_dict.json()
    dm_names = dm_detail['name']
    assert dm_names == 'defwoo, rafwoo, rafwoo0'
