import requests
import pytest
import json
from src import config
from src.other import clear_v1

@pytest.fixture
def setup():
    requests.delete(config.url + 'clear/v1')

@pytest.fixture
def token():
    #create user1
    response = requests.post(config.url + 'auth/register/v2', json = {"email" : "user1@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    auid_dict = response.json()
    token = auid_dict['token']
    return token

@pytest.fixture
def uid2():
    #create user2
    response = requests.post(config.url + 'auth/register/v2', json = {"email" : "user2@gmail.com", "password" : "Password123", "name_first" : "Bobby", "name_last" : "Smithy"})
    auid_dict = response.json()
    user_id2 = auid_dict['auth_user_id']
    return user_id2

@pytest.fixture
def token2():
    #create user2
	response = requests.post(config.url + 'auth/register/v2', json = {"email" : "user3@gmail.com", "password" : "Password123", "name_first" : "Bobby", "name_last" : "Smithy"})
	auid_dict = response.json()
	token2 = auid_dict['token']
	return token2

def test_dm_messages_invalid_token(setup, token, uid2):
	response = requests.post(config.url + 'dm/create/v1', json = {"token" : token, "u_ids" : [uid2]})
	dmid_dict = response.json()
	dm_id1 = dmid_dict['dm_id']
	dict = {'token' : token + 'wrong', 'dm_id' : dm_id1, 'start' : 0}
	dm_message_response = requests.get(config.url + 'dm/messages/v1', params=dict)
	assert dm_message_response.status_code == 403

def test_dm_messages_invalid_dmid(setup, token, uid2):
	response = requests.post(config.url + 'dm/create/v1', json = {"token" : token, "u_ids" : [uid2]})
	dmid_dict = response.json()
	dm_id1 = dmid_dict['dm_id']
	dict = {'token' : token, 'dm_id' : dm_id1 + 1, 'start' : 0}
	dm_message_response = requests.get(config.url + 'dm/messages/v1', params=dict)
	assert dm_message_response.status_code == 400

def test_dm_messages_invalid_start(setup, token, uid2):
	response = requests.post(config.url + 'dm/create/v1', json = {"token" : token, "u_ids" : [uid2]})
	dmid_dict = response.json()
	dm_id1 = dmid_dict['dm_id']
	dict = {'token' : token, 'dm_id' : dm_id1, 'start' : 10}
	dm_message_response = requests.get(config.url + 'dm/messages/v1', params=dict)
	assert dm_message_response.status_code == 400

def test_dm_messages_not_member(setup, token, uid2, token2):
	response = requests.post(config.url + 'dm/create/v1', json = {"token" : token, "u_ids" : [uid2]})
	dmid_dict = response.json()
	dm_id1 = dmid_dict['dm_id']
	dict = {'token' : token2, 'dm_id' : dm_id1, 'start' : 0}
	dm_message_response = requests.get(config.url + 'dm/messages/v1', params=dict)
	assert dm_message_response.status_code == 403

def test_valid_dm_message(setup, token, uid2):
	response = requests.post(config.url + 'dm/create/v1', json = {"token" : token, "u_ids" : [uid2]})
	dmid_dict = response.json()
	dm_id1 = dmid_dict['dm_id']
	dict = {'token' : token, 'dm_id' : dm_id1, 'start' : 0}
	dm_message_response = requests.get(config.url + 'dm/messages/v1', params=dict)
	dm_messages = dm_message_response.json()
	assert dm_messages == {"messages" : [], "start" : 0, "end" : -1}

def test_valid_message_v2_2(setup, token, uid2):
	#create dm
	response = requests.post(config.url + 'dm/create/v1', json = {"token" : token, "u_ids" : [uid2]})
	dmid_dict = response.json()
	dm_id = dmid_dict['dm_id']
	for i in range(0, 51):
		requests.post(config.url + 'message/senddm/v1', json = {"token": token, "dm_id": dm_id, "message": "msg"})
		i = i+1
	# call channel_messages_v2
	dict = {'token' : token, 'dm_id' : dm_id, 'start' : 0}
	response3 = requests.get(config.url + 'dm/messages/v1', params=dict)
	messages_dict = response3.json()
	start = messages_dict['start']
	end = messages_dict['end']
	assert (start == 0 and end == 50)