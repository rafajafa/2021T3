import requests
import pytest
import json
from json import dumps
from src import config

# Test that the dm owner can edit their own message.
def test_message_edit_dm_owner_success():
    requests.delete(config.url + 'clear/v1')

    response1 = requests.post(config.url + 'auth/register/v2', json={"email" : "user1@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    register_ret1 = response1.json()
    token1 = register_ret1['token']

    response2 = requests.post(config.url + 'auth/register/v2', json={"email" : "user2@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    register_ret2 = response2.json()
    token2 = register_ret2['token']
    auid2 = register_ret2['auth_user_id']

    dm_create_response = requests.post(config.url + 'dm/create/v1', json={"token" : token1, "u_ids": [auid2]})
    dm_create_ret = dm_create_response.json()
    dm_id = dm_create_ret['dm_id']

    dm_message_response = requests.post(config.url + 'message/senddm/v1', json={"token" : token2, "dm_id": dm_id, "message": "Hey"})
    dm_message_response_json = dm_message_response.json()
    message_id = dm_message_response_json['message_id']

    dict = {'token' : token1, 'dm_id' : dm_id, 'start' : 0}
    dm_messages_pre_edit_response = requests.get(config.url + 'dm/messages/v1', params=dict)
    dm_messages_pre_edit_response_json = dm_messages_pre_edit_response.json()
    assert dm_messages_pre_edit_response_json['messages'][0]['message'] == "Hey"

    dm_message_edit_response = requests.put(config.url + 'message/edit/v1', json={"token" : token1, "message_id": message_id, "message": "Hello"})
    assert dm_message_edit_response.status_code == 200
    
    dm_messages_post_edit_response = requests.get(config.url + 'dm/messages/v1', params=dict)
    dm_messages_post_edit_response_json = dm_messages_post_edit_response.json()
    assert dm_messages_post_edit_response_json['messages'][0]['message'] == "Hello"

# Test that a non dm owner cannot edit a message they don't own. (double check)
def test_message_edit_non_dm_owner_fail():
    requests.delete(config.url + 'clear/v1')

    response1 = requests.post(config.url + 'auth/register/v2', json={"email" : "user1@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    register_ret1 = response1.json()
    token1 = register_ret1['token']

    response2 = requests.post(config.url + 'auth/register/v2', json={"email" : "user2@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    register_ret2 = response2.json()
    token2 = register_ret2['token']
    auid2 = register_ret2['auth_user_id']

    dm_create_response = requests.post(config.url + 'dm/create/v1', json={"token" : token1, "u_ids": [auid2]})
    dm_create_ret = dm_create_response.json()
    dm_id = dm_create_ret['dm_id']

    dm_message_response = requests.post(config.url + 'message/senddm/v1', json={"token" : token1, "dm_id": dm_id, "message": "Hey"})
    dm_message_response_json = dm_message_response.json()
    message_id = dm_message_response_json['message_id']

    dict = {'token' : token1, 'dm_id' : dm_id, 'start' : 0}
    dm_messages_pre_edit_response = requests.get(config.url + 'dm/messages/v1', params=dict)
    dm_messages_pre_edit_response_json = dm_messages_pre_edit_response.json()
    assert dm_messages_pre_edit_response_json['messages'][0]['message'] == "Hey"

    dm_message_edit_response = requests.put(config.url + 'message/edit/v1', json={"token" : token2, "message_id": message_id, "message": "Hello"})
    assert dm_message_edit_response.status_code == 403
    
    dm_messages_post_edit_response = requests.get(config.url + 'dm/messages/v1', params=dict)
    dm_messages_post_edit_response_json = dm_messages_post_edit_response.json()
    assert dm_messages_post_edit_response_json['messages'][0]['message'] == "Hey"

# Test that message owner can edit their own message.
def test_message_edit_message_owner_success():
    requests.delete(config.url + 'clear/v1')

    response1 = requests.post(config.url + 'auth/register/v2', json={"email" : "user1@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    register_ret1 = response1.json()
    token1 = register_ret1['token']

    response2 = requests.post(config.url + 'auth/register/v2', json={"email" : "user2@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    register_ret2 = response2.json()
    token2 = register_ret2['token']
    auid2 = register_ret2['auth_user_id']

    channel_create_response = requests.post(config.url + 'channels/create/v2', json={"token" : token1, "name": "Channel 1", "is_public": True})
    channel_create_ret = channel_create_response.json()
    channel_id = channel_create_ret['channel_id']

    requests.post(config.url + 'channel/invite/v2', json={"token" : token1, "channel_id": channel_id, "u_id": auid2})

    channel_message_response = requests.post(config.url + 'message/send/v1', json={"token" : token2, "channel_id": channel_id, "message": "Hey"})
    channel_message_response_json = channel_message_response.json()
    message_id = channel_message_response_json['message_id']

    dict = {'token' : token2, 'channel_id' : channel_id, 'start' : 0}
    channel_messages_pre_edit_response = requests.get(config.url + 'channel/messages/v2', params=dict)
    channel_messages_pre_edit_response_json = channel_messages_pre_edit_response.json()
    assert channel_messages_pre_edit_response_json['messages'][0]['message'] == "Hey"

    channel_message_edit_response = requests.put(config.url + 'message/edit/v1', json={"token" : token2, "message_id": message_id, "message": "Hello"})
    assert channel_message_edit_response.status_code == 200
    
    dict = {'token' : token2, 'channel_id' : channel_id, 'start' : 0}
    channel_messages_post_edit_response = requests.get(config.url + 'channel/messages/v2', params=dict)
    channel_messages_post_edit_response_json = channel_messages_post_edit_response.json()
    assert channel_messages_post_edit_response_json['messages'][0]['message'] == "Hello"

# Test that the channel owner can edit a message that they don't own. 
def test_message_edit_channel_owner_success():
    requests.delete(config.url + 'clear/v1')

    response1 = requests.post(config.url + 'auth/register/v2', json={"email" : "user1@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    register_ret1 = response1.json()
    token1 = register_ret1['token']

    response2 = requests.post(config.url + 'auth/register/v2', json={"email" : "user2@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    register_ret2 = response2.json()
    token2 = register_ret2['token']
    auid2 = register_ret2['auth_user_id']

    channel_create_response = requests.post(config.url + 'channels/create/v2', json={"token" : token1, "name": "Channel 1", "is_public": True})
    channel_create_ret = channel_create_response.json()
    channel_id = channel_create_ret['channel_id']

    requests.post(config.url + 'channel/invite/v2', json={"token" : token1, "channel_id": channel_id, "u_id": auid2})

    channel_message_response = requests.post(config.url + 'message/send/v1', json={"token" : token2, "channel_id": channel_id, "message": "Hey"})
    channel_message_response_json = channel_message_response.json()
    message_id = channel_message_response_json['message_id']

    dict = {'token' : token1, 'channel_id' : channel_id, 'start' : 0}
    channel_messages_pre_edit_response = requests.get(config.url + 'channel/messages/v2', params=dict)
    channel_messages_pre_edit_response_json = channel_messages_pre_edit_response.json()
    assert channel_messages_pre_edit_response_json['messages'][0]['message'] == "Hey"

    channel_message_edit_response = requests.put(config.url + 'message/edit/v1', json={"token" : token1, "message_id": message_id, "message": "Hello"})
    assert channel_message_edit_response.status_code == 200
    
    channel_messages_post_edit_response = requests.get(config.url + 'channel/messages/v2', params=dict)
    channel_messages_post_edit_response_json = channel_messages_post_edit_response.json()
    assert channel_messages_post_edit_response_json['messages'][0]['message'] == "Hello"

# # Test if a message in a channel can be edited.
def test_channel_message_invalid():
    requests.delete(config.url + 'clear/v1')
    
    # If the message is too long (> 1000 chars)
    long_message = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

    response1 = requests.post(config.url + 'auth/register/v2', json={"email" : "user1@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    register_ret1 = response1.json()
    token1 = register_ret1['token']

    response2 = requests.post(config.url + 'auth/register/v2', json={"email" : "user2@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    register_ret2 = response2.json()
    token2 = register_ret2['token']
    auid2 = register_ret2['auth_user_id']

    channel_response = requests.post(config.url + 'channels/create/v2', json = {"token": token1, "name": "channel1", "is_public": True})
    channel_return = channel_response.json()
    cid = channel_return['channel_id']
    
    requests.post(config.url + 'channel/invite/v2', json={"token" : token1, "channel_id": cid, "u_id": auid2})

    channel_message_response = requests.post(config.url + 'message/send/v1', json={"token" : token2, "channel_id": cid, "message": "Hey"})
    channel_message_response_json = channel_message_response.json()
    message_id = channel_message_response_json['message_id']

    dict = {'token' : token2, 'channel_id' : cid, 'start' : 0}
    channel_messages_pre_edit_response = requests.get(config.url + 'channel/messages/v2', params=dict)
    channel_messages_pre_edit_response_json = channel_messages_pre_edit_response.json()
    assert channel_messages_pre_edit_response_json['messages'][0]['message'] == "Hey"

    channel_message_edit_response = requests.put(config.url + 'message/edit/v1', json={"token" : token2, "message_id": message_id, "message": long_message})
    assert channel_message_edit_response.status_code == 400

    channel_messages_post_edit_response = requests.get(config.url + 'channel/messages/v2', params=dict)
    channel_messages_post_edit_response_json = channel_messages_post_edit_response.json()
    assert channel_messages_post_edit_response_json['messages'][0]['message'] == "Hey"

# Test if a message in a dm can be edited. 
def test_dm_message_invalid():
    requests.delete(config.url + 'clear/v1')
    
    # If the message is too long (> 1000 chars)
    long_message = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

    response1 = requests.post(config.url + 'auth/register/v2', json={"email" : "user1@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    register_ret1 = response1.json()
    token1 = register_ret1['token']

    response2 = requests.post(config.url + 'auth/register/v2', json={"email" : "user2@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    register_ret2 = response2.json()
    token2 = register_ret2['token']
    auid2 = register_ret2['auth_user_id']

    dm_create_response = requests.post(config.url + 'dm/create/v1', json={"token" : token1, "u_ids": [auid2]})
    dm_create_ret = dm_create_response.json()
    dm_id = dm_create_ret['dm_id']

    dm_message_response = requests.post(config.url + 'message/senddm/v1', json={"token" : token2, "dm_id": dm_id, "message": "Hey"})
    dm_message_response_json = dm_message_response.json()
    message_id = dm_message_response_json['message_id']

    dict = {'token' : token1, 'dm_id' : dm_id, 'start' : 0}
    dm_messages_pre_edit_response = requests.get(config.url + 'dm/messages/v1', params=dict)
    dm_messages_pre_edit_response_json = dm_messages_pre_edit_response.json()
    assert dm_messages_pre_edit_response_json['messages'][0]['message'] == "Hey"

    dm_message_edit_response = requests.put(config.url + 'message/edit/v1', json={"token" : token1, "message_id": message_id, "message": long_message})
    assert dm_message_edit_response.status_code == 400
    
    dm_messages_post_edit_response = requests.get(config.url + 'dm/messages/v1', params=dict)
    dm_messages_post_edit_response_json = dm_messages_post_edit_response.json()
    assert dm_messages_post_edit_response_json['messages'][0]['message'] == "Hey"