import pytest
import json
import requests
import sys
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError, AccessError
from src import config

# Test to ensure that the function removes users, alters their profile and deletes their messages as expected
def test_admin_user_remove_works():
    requests.delete(config.url + 'clear/v1')

    # Register two users
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "first_name", "name_last": "last_name"})
    resp1 = response1.json()
    token1 = resp1['token']

    response2 = requests.post(config.url + 'auth/register/v2', json = {"email": "def@gmail.com", "password": "thepassword", "name_first": "first_name", "name_last": "last_name"})
    resp2 = response2.json()
    auid2 = resp2['auth_user_id']
    token2 = resp2['token']

    # Create a channel, and let the second user send a message to it
    channel_response = requests.post(config.url + 'channels/create/v2', json = {"token": token1, "name": "channel1", "is_public": False})
    channel_return = channel_response.json()
    cid = channel_return['channel_id']

    requests.post(config.url + 'channel/invite/v2', json = {"token": token1, "channel_id": cid, "u_id": auid2})
    requests.post(config.url + 'message/send/v1', json = {"token": token2, "channel_id": cid, "message": "Hello"})

    # Do the same with a dm
    dm_create_response = requests.post(config.url + 'dm/create/v1', json={"token": token1, "u_ids": [auid2]})
    dm_create_return = dm_create_response.json()
    dm_id = dm_create_return['dm_id']

    requests.post(config.url + 'message/senddm/v1', json={"token": token2, "dm_id": dm_id, "message": "World"})
    
    # Remove the second user
    remove_response = requests.delete(config.url + 'admin/user/remove/v1', json={"token": token1, "u_id": auid2})
    assert remove_response.status_code == 200

    # Check that their channel message has changed its content to 'Removed user'
    dict = {'token' : token1, 'channel_id' : cid, 'start' : 0}
    channel_messages_response = requests.get(config.url + 'channel/messages/v2', params=dict)
    channel_messages_return = channel_messages_response.json()
    messages = channel_messages_return['messages']
    only_message = messages[0]
    assert only_message['message'] == 'Removed user'

    # Do the same with the dm
    dict = {'token' : token1, 'dm_id' : dm_id, 'start' : 0}
    dm_messages_response = requests.get(config.url + 'dm/messages/v1', params=dict)
    dm_messages_return = dm_messages_response.json()
    messages = dm_messages_return['messages']
    only_message = messages[0]
    assert only_message['message'] == 'Removed user'

    # Check that the user's profile details are removed
    dict = {'token' : token1, 'u_id' : auid2}
    user_profile_response = requests.get(config.url + 'user/profile/v1', params=dict)
    user_profile_return = user_profile_response.json()
    user = user_profile_return['user']
    assert user['name_first'] == 'Removed'
    assert user['name_last'] == 'user'

# Test for an InputError when the u_id given does not belong to a registered user
def test_non_registered_u_id():
    requests.delete(config.url + 'clear/v1')

    # Register a user
    response = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "first_name", "name_last": "last_name"})
    resp = response.json()
    auid = resp['auth_user_id']
    token = resp['token']

    # Pass in an invalid u_id (i.e. does not belong to any registered user)
    remove_response = requests.delete(config.url + 'admin/user/remove/v1', json={"token": token, "u_id": auid+1})
    assert remove_response.status_code == 400
    

# Test for an InputError when the sole global owner attempts to remove themselves
def test_sole_global_owner():
    requests.delete(config.url + 'clear/v1')

    # Register a user (the Streams owner)
    response = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "first_name", "name_last": "last_name"})
    resp = response.json()
    auid = resp['auth_user_id']
    token = resp['token']

    # Pass in the Streams owner's own user id
    remove_response = requests.delete(config.url + 'admin/user/remove/v1', json={"token": token, "u_id": auid})
    assert remove_response.status_code == 400


# Tests if an AccessError is thrown when both Input and Access Errors apply
# Specifically, if a non-global owner uses this function to remove the only global owner
def test_non_global_removing_sole_global():
    requests.delete(config.url + 'clear/v1')

    # Register two users
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "first_name", "name_last": "last_name"})
    resp1 = response1.json()
    auid1 = resp1['auth_user_id']

    response2 = requests.post(config.url + 'auth/register/v2', json = {"email": "def@gmail.com", "password": "thepassword", "name_first": "first_name", "name_last": "last_name"})
    resp2 = response2.json()
    token2 = resp2['token']

    # The non-owner attempts to remove the only global owner
    remove_response = requests.delete(config.url + 'admin/user/remove/v1', json={"token": token2, "u_id": auid1})
    assert remove_response.status_code == 403


# Test for an AccessError when an invalid token from an expired session is given
def test_expired_token():
    requests.delete(config.url + 'clear/v1')

    # Register two users
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "first_name", "name_last": "last_name"})
    resp1 = response1.json()
    auid1 = resp1['auth_user_id']
    token1 = resp1['token']

    response2 = requests.post(config.url + 'auth/register/v2', json = {"email": "def@gmail.com", "password": "thepassword", "name_first": "first_name", "name_last": "last_name"})
    resp2 = response2.json()
    token2 = resp2['token']

    # The owner logs out
    requests.post(config.url + 'auth/logout/v1', json = {"token": token1})

    # The owner's expired token is used to remove the non-owner user
    remove_response = requests.delete(config.url + 'admin/user/remove/v1', json={"token": token2, "u_id": auid1})
    assert remove_response.status_code == 403

# Test for an AccessError when a token is given which doesn't encode any registration details
def test_meaningless_token():
    requests.delete(config.url + 'clear/v1')

    # Register two users
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "first_name", "name_last": "last_name"})
    resp1 = response1.json()
    auid1 = resp1['auth_user_id']

    response2 = requests.post(config.url + 'auth/register/v2', json = {"email": "def@gmail.com", "password": "thepassword", "name_first": "first_name", "name_last": "last_name"})
    resp2 = response2.json()
    token2 = resp2['token']

    # When the users' tokens are concatenated, a 'meaningless' token is formed 
    remove_response = requests.delete(config.url + 'admin/user/remove/v1', json={"token": token2 + 'wrong', "u_id": auid1})
    assert remove_response.status_code == 403

# Test for an AccessError when a non-global user's token is given
def test_non_global_usage():
    requests.delete(config.url + 'clear/v1')

    # Register three users
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "first_name", "name_last": "last_name"})
    resp1 = response1.json()
    auid1 = resp1['auth_user_id']
    token1 = resp1['token']

    response2 = requests.post(config.url + 'auth/register/v2', json = {"email": "def@gmail.com", "password": "thepassword", "name_first": "first_name", "name_last": "last_name"})
    resp2 = response2.json()
    auid2 = resp2['auth_user_id']
    token2 = resp2['token']

    remove_response1 = requests.delete(config.url + 'admin/user/remove/v1', json={"token": token2, "u_id": auid1})
    assert remove_response1.status_code == 403

    requests.post(config.url + 'admin/userpermission/change/v1', json={"token": token1, "u_id": auid2, "permission_id" : 1})

    remove_response2 = requests.delete(config.url + 'admin/user/remove/v1', json={"token": token2, "u_id": auid1})
    assert remove_response2.status_code == 200
