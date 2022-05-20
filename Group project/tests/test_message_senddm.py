import requests
import pytest
from requests.models import parse_header_links
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

def test_invalid_dmid(setup, token, uid2):
    #call dm/create/v1
    dm_response = requests.post(config.url + 'dm/create/v1', json = {"token" : token, "u_ids" : [uid2]})
    dmid_dict = dm_response.json()
    dmid = dmid_dict['dm_id']
    #call message/senddm/v1
    senddm_response = requests.post(config.url + 'message/senddm/v1', json = {"token" : token, "dm_id" : dmid+1, "message" : "message"})
    #input error
    assert (senddm_response.status_code == 400)


def test_invalid_message_short(setup, token, uid2):
    #call dm/create/v1
    dm_response = requests.post(config.url + 'dm/create/v1', json = {"token" : token, "u_ids" : [uid2]})
    dmid_dict = dm_response.json()
    dmid = dmid_dict['dm_id']
    #call message/senddm/v1
    senddm_response = requests.post(config.url + 'message/senddm/v1', json = {"token" : token, "dm_id" : dmid, "message" : ""})
    #input error
    assert (senddm_response.status_code == 400)

def test_invalid_message_long(setup, token, uid2):
    #call dm/create/v1
    dm_response = requests.post(config.url + 'dm/create/v1', json = {"token" : token, "u_ids" : [uid2]})
    dmid_dict = dm_response.json()
    dmid = dmid_dict['dm_id']
    #call message/senddm/v1
    senddm_response = requests.post(config.url + 'message/senddm/v1', json = {"token" : token, "dm_id" : dmid, "message" : "a"*1001})
    #input error
    assert (senddm_response.status_code == 400)

def test_valid_senddm(setup, token, uid2):
    #call dm/create/v1
    dm_response = requests.post(config.url + 'dm/create/v1', json = {"token" : token,  "u_ids" : [uid2]})
    dmid_dict = dm_response.json()
    dmid = dmid_dict['dm_id']
    #call message/senddm/v1
    senddm_response = requests.post(config.url + 'message/senddm/v1', json = {"token" : token, "dm_id" : dmid, "message" : "message"})
    senddm_dict = senddm_response.json()
    message_id = senddm_dict['message_id']
    assert message_id == 1

    dict = {'token' : token, 'dm_id' : dmid, 'start' : 0}
    dm_messages_response = requests.get(config.url + 'dm/messages/v1', params=dict)
    dm_messages_dict = dm_messages_response.json()
    dm_messages = dm_messages_dict['messages']
    message_dict = dm_messages[0]
    message = message_dict['message']
    assert message == 'message'

def test_valid_dmid_different_dmchannel(setup, token, uid2):
    #call dm/create/v1
    dm_response = requests.post(config.url + 'dm/create/v1', json = {"token" : token, "u_ids" : [uid2]})
    dmid_dict = dm_response.json()
    dmid = dmid_dict['dm_id']
    #call message/senddm/v1 with wrong token
    senddm_response = requests.post(config.url + 'message/senddm/v1', json = {"token" : token + "wrong", "dm_id" : dmid, "message" : "message"})
    #access error
    assert (senddm_response.status_code == 403)
