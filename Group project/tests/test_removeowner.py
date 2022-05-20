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

# Fixture to register two users and create a channel with both as owners
@pytest.fixture
def register_two_channel_owners():
    requests.delete(config.url + 'clear/v1')
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "stonk", "name_last": "mcstonker"})
    resp1 = response1.json()
    token1 = resp1['token']
    response2 = requests.post(config.url + 'auth/register/v2', json = {"email": "def@gmail.com", "password": "thepassword1", "name_first": "stonk", "name_last": "mcstonker"})
    resp2 = response2.json()
    auid2 = resp2['auth_user_id']
    token2 = resp2['token']

    channel_response = requests.post(config.url + 'channels/create/v2', json = {"token": token1, "channel": "channel1", "is_public": False})
    channel_return = channel_response.json()
    cid = channel_return['channel_id']
    requests.post(config.url + 'channel/invite/v2', json = {"token": token1, "channel_id": cid,"u_id": auid2})
    requests.post(config.url + 'channels/addowner/v1', json = {"token": token1, "channel_id": cid, "u_id": auid2})

    return {'token1': token1, 'token2': token2}


# Tests if the function actually does remove an owner as expected
def test_removeowner_works():
    requests.delete(config.url + 'clear/v1')
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "stonk", "name_last": "mcstonker"})
    resp1 = response1.json()
    token1 = resp1['token']
    auid1 = resp1['auth_user_id']
    response2 = requests.post(config.url + 'auth/register/v2', json = {"email": "def@gmail.com", "password": "thepassword1", "name_first": "stonk", "name_last": "mcstonker"})
    resp2 = response2.json()
    auid2 = resp2['auth_user_id']

    channel_response = requests.post(config.url + 'channels/create/v2', json = {"token": token1, "name": "channel1", "is_public": False})
    channel_return = channel_response.json()
    cid = channel_return['channel_id']
    requests.post(config.url + 'channel/invite/v2', json = {"token": token1, "channel_id": cid,"u_id": auid2})
    requests.post(config.url + 'channel/addowner/v1', json = {"token": token1, "channel_id": cid, "u_id": auid2})

    ###########
    remove_response = requests.post(config.url + 'channel/removeowner/v1', json = {"token": token1, "channel_id": cid, "u_id": auid2})
    assert remove_response.status_code == 200

    dict = {'token' : token1, 'channel_id' : cid}
    details_response = requests.get(config.url + 'channel/details/v2', params=dict)
    details = details_response.json()
    owners = details['owner_members']
    assert owners == [{"u_id": auid1, "email": "abc@gmail.com", "name_first": "stonk", "name_last": "mcstonker", "handle_str": "stonkmcstonker"}]

# Tests for an AccessError when an invalid token is given as input
def test_invalid_token():
    requests.delete(config.url + 'clear/v1')
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "stonk", "name_last": "mcstonker"})
    resp1 = response1.json()
    token1 = resp1['token']
    response2 = requests.post(config.url + 'auth/register/v2', json = {"email": "def@gmail.com", "password": "thepassword1", "name_first": "stonk", "name_last": "mcstonker"})
    resp2 = response2.json()
    auid2 = resp2['auth_user_id']

    channel_response = requests.post(config.url + 'channels/create/v2', json = {"token": token1, "name": "channel1", "is_public": False})
    channel_return = channel_response.json()
    cid = channel_return['channel_id']
    requests.post(config.url + 'channel/invite/v2', json = {"token": token1, "channel_id": cid,"u_id": auid2})
    requests.post(config.url + 'channel/addowner/v1', json = {"token": token1, "channel_id": cid, "u_id": auid2})
    ###########
    remove_response = requests.post(config.url + 'channel/removeowner/v1', json = {"token": token1 + "wrong", "channel_id": cid, "u_id": auid2})
    assert remove_response.status_code == 403


# Tests if an InputError is raised when the u_id of the owner to be removed does not belong to a registered user
def test_unregistered_uid():
    requests.delete(config.url + 'clear/v1')
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "stonk", "name_last": "mcstonker"})
    resp1 = response1.json()
    token1 = resp1['token']
    auid1 = resp1['auth_user_id']
    response2 = requests.post(config.url + 'auth/register/v2', json = {"email": "def@gmail.com", "password": "thepassword1", "name_first": "stonk", "name_last": "mcstonker"})
    resp2 = response2.json()
    auid2 = resp2['auth_user_id']

    channel_response = requests.post(config.url + 'channels/create/v2', json = {"token": token1, "name": "channel1", "is_public": False})
    channel_return = channel_response.json()
    cid = channel_return['channel_id']
    requests.post(config.url + 'channel/invite/v2', json = {"token": token1, "channel_id": cid,"u_id": auid2})
    requests.post(config.url + 'channel/addowner/v1', json = {"token": token1, "channel_id": cid, "u_id": auid2})
    #################################
    remove_response = requests.post(config.url + 'channel/removeowner/v1', json = {"token": token1, "channel_id": cid, "u_id": auid2+auid1+1})
    assert remove_response.status_code == 400
    
# Tests if an InputError is raised when the u_id of the owner to be removed does not belong to a channel owner
def test_non_owner_uid():
    requests.delete(config.url + 'clear/v1')
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "stonk", "name_last": "mcstonker"})
    resp1 = response1.json()
    token1 = resp1['token']
    response2 = requests.post(config.url + 'auth/register/v2', json = {"email": "def@gmail.com", "password": "thepassword1", "name_first": "stonk", "name_last": "mcstonker"})
    resp2 = response2.json()
    auid2 = resp2['auth_user_id']

    channel_response = requests.post(config.url + 'channels/create/v2', json = {"token": token1, "name": "channel1", "is_public": False})
    channel_return = channel_response.json()
    cid = channel_return['channel_id']
    requests.post(config.url + 'channel/invite/v2', json = {"token": token1, "channel_id": cid,"u_id": auid2})
    remove_response = requests.post(config.url + 'channel/removeowner/v1', json = {"token": token1, "channel_id": cid, "u_id": auid2})
    assert remove_response.status_code == 400


# Tests if an InputError is raised when the sole owner of a channel attempts to remove themselves
def test_remove_sole_owner():
    requests.delete(config.url + 'clear/v1')
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "stonk", "name_last": "mcstonker"})
    resp1 = response1.json()
    token1 = resp1['token']
    auid1 = resp1['auth_user_id']

    channel_response = requests.post(config.url + 'channels/create/v2', json = {"token": token1, "name": "channel1", "is_public": False})
    channel_return = channel_response.json()
    cid = channel_return['channel_id']
    #######################################
    remove_response = requests.post(config.url + 'channel/removeowner/v1', json = {"token": token1, "channel_id": cid, "u_id": auid1})
    assert remove_response.status_code == 400

# Tests if an AccessError is thrown when both Input and Access Errors apply
# Specifically, if a non-owner channel member is attempting to remove the only owner of the channel
def test_non_owner_removing_owner():
    requests.delete(config.url + 'clear/v1')
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "stonk", "name_last": "mcstonker"})
    resp1 = response1.json()
    token1 = resp1['token']
    auid1 = resp1['auth_user_id']
    response2 = requests.post(config.url + 'auth/register/v2', json = {"email": "def@gmail.com", "password": "thepassword1", "name_first": "stonk", "name_last": "mcstonker"})
    resp2 = response2.json()
    auid2 = resp2['auth_user_id']
    token2 = resp2['token']

    channel_response = requests.post(config.url + 'channels/create/v2', json = {"token": token1, "name": "channel1", "is_public": False})
    channel_return = channel_response.json()
    cid = channel_return['channel_id']
    requests.post(config.url + 'channel/invite/v2', json = {"token": token1, "channel_id": cid,"u_id": auid2})
    ###########################
    remove_response = requests.post(config.url + 'channel/removeowner/v1', json = {"token": token2, "channel_id": cid, "u_id": auid1})
    assert remove_response.status_code == 403


# Tests if an InputError is thrown when a channel_id for a non-existent channel is given as input
def test_invalid_channel_id():
    requests.delete(config.url + 'clear/v1')
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "stonk", "name_last": "mcstonker"})
    resp1 = response1.json()
    token1 = resp1['token']
    response2 = requests.post(config.url + 'auth/register/v2', json = {"email": "def@gmail.com", "password": "thepassword1", "name_first": "stonk", "name_last": "mcstonker"})
    resp2 = response2.json()
    auid2 = resp2['auth_user_id']

    channel_response = requests.post(config.url + 'channels/create/v2', json = {"token": token1, "name": "channel1", "is_public": False})
    channel_return = channel_response.json()
    cid = channel_return['channel_id']
    requests.post(config.url + 'channel/invite/v2', json = {"token": token1, "channel_id": cid,"u_id": auid2})
    requests.post(config.url + 'channel/addowner/v1', json = {"token": token1, "channel_id": cid, "u_id": auid2})
    ###########################
    remove_response = requests.post(config.url + 'channel/removeowner/v1', json = {"token": token1, "channel_id": cid+1, "u_id": auid2})
    assert remove_response.status_code == 400
