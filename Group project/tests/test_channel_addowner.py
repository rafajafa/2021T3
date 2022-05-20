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
def token2():
    #create user2
    response = requests.post(config.url + 'auth/register/v2', json = {"email" : "user2@gmail.com", "password" : "Password123", "name_first" : "Bobby", "name_last" : "Smithy"})
    auid_dict = response.json()
    token2 = auid_dict['token']
    return token2

@pytest.fixture
def uid2():
    #create user2
    response = requests.post(config.url + 'auth/register/v2', json = {"email" : "user3@gmail.com", "password" : "Password123", "name_first" : "Bobby", "name_last" : "Smithy"})
    auid_dict = response.json()
    user_id2 = auid_dict['auth_user_id']
    return user_id2

@pytest.fixture
def uid3():
    #create user2
    response = requests.post(config.url + 'auth/register/v2', json = {"email" : "user4@gmail.com", "password" : "Password123", "name_first" : "Bobbo", "name_last" : "Smithy"})
    auid_dict = response.json()
    user_id3 = auid_dict['auth_user_id']
    return user_id3

def test_addowner_invalid_token(setup, token, uid2):
    channel_response = requests.post(config.url + 'channels/create/v2', json = {"token" : token, "name" : "channelname", "is_public" : True})
    create_return = channel_response.json()
    channel_id = create_return['channel_id']
    response = requests.post(config.url + 'channel/addowner/v1', json = {"token" : token + "wrong", "channel_id" : channel_id, "u_id" : uid2})
    assert response.status_code == 403

def test_addowner_invalid_channel_id(setup, token, uid2):
    channel_response = requests.post(config.url + 'channels/create/v2', json = {"token" : token, "name" : "channelname", "is_public" : True})
    create_return = channel_response.json()
    channel_id = create_return['channel_id']
    response = requests.post(config.url + 'channel/addowner/v1', json = {"token" : token, "channel_id" : channel_id+1, "u_id" : uid2})
    assert response.status_code == 400

def test_addowner_invalid_uid(setup, token, uid2):
    channel_response = requests.post(config.url + 'channels/create/v2', json = {"token" : token, "name" : "channelname", "is_public" : True})
    create_return = channel_response.json()
    channel_id = create_return['channel_id']
    response = requests.post(config.url + 'channel/addowner/v1', json = {"token" : token, "channel_id" : channel_id, "u_id" : uid2+1})
    assert response.status_code == 400

def test_addowner_user_not_member(setup, token, uid2):
    channel_response = requests.post(config.url + 'channels/create/v2', json = {"token" : token, "name" : "channelname", "is_public" : False})
    create_return = channel_response.json()
    channel_id = create_return['channel_id']
    response = requests.post(config.url + 'channel/addowner/v1', json = {"token" : token, "channel_id" : channel_id, "u_id" : uid2})
    assert response.status_code == 400

def test_add_owner_already_owner(setup, token, uid2):
    channel_response = requests.post(config.url + 'channels/create/v2', json = {"token" : token, "name" : "channelname", "is_public" : False})
    create_return = channel_response.json()
    channel_id = create_return['channel_id']
    requests.post(config.url + 'channel/invite/v2', json = {"token" : token, "channel_id" : channel_id, "u_id" : uid2})
    requests.post(config.url + 'channel/addowner/v1', json = {"token" : token, "channel_id" : channel_id, "u_id" : uid2})
    response = requests.post(config.url + 'channel/addowner/v1', json = {"token" : token, "channel_id" : channel_id, "u_id" : uid2})
    assert response.status_code == 400

def test_valid_channel_user_not_owner(setup, token, token2, uid3):
    channel_response = requests.post(config.url + 'channels/create/v2', json = {"token" : token, "name" : "channelname", "is_public" : True})
    create_return = channel_response.json()
    channel_id = create_return['channel_id']
    response = requests.post(config.url + 'channel/join/v2', json = {"token" : token2, "channel_id" : channel_id})
    response = requests.post(config.url + 'channel/addowner/v1', json = {"token" : token2, "channel_id" : channel_id, "u_id" : uid3})
    assert response.status_code == 403


def test_channel_addowner_valid(setup, uid2):
    #Check with Rafael
    response = requests.post(config.url + 'auth/register/v2', json = {"email" : "user1@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    auid_dict = response.json()
    token = auid_dict['token']
    channel_response = requests.post(config.url + 'channels/create/v2', json = {"token" : token, "name" : "channelname", "is_public" : True})
    create_return = channel_response.json()
    channel_id = create_return['channel_id']
    response = requests.post(config.url + 'channel/invite/v2', json = {"token" : token, "channel_id" : channel_id, "u_id" : uid2})
    assert response.status_code == 200
    response = requests.post(config.url + 'channel/addowner/v1', json = {"token" : token, "channel_id" : channel_id, "u_id" : uid2})
    assert response.status_code == 200

    dict = {'token' : token, 'channel_id' : channel_id}
    details_response = requests.get(config.url + 'channel/details/v2', params=dict)
    details = details_response.json()
    owners = details['owner_members']
    assert owners == [{'u_id': 2, 'email': 'user1@gmail.com', 'name_first': 'Bob', 'name_last': 'Smith', 'handle_str': 'bobsmith'}, 
        {'u_id': 1, 'email': 'user3@gmail.com', 'name_first': 'Bobby', 'name_last': 'Smithy', 'handle_str': 'bobbysmithy'}]
