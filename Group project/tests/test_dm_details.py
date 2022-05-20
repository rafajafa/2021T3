import requests
import pytest
import json
from json import dumps
from src import config

# Tests for an InputError when an invalid dm_id is given
def test_dm_details_invalid_dm_id():
    requests.delete(config.url + 'clear/v1')

    response1 = requests.post(config.url + 'auth/register/v2', json={"email" : "user1@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    register_ret1 = response1.json()
    token1 = register_ret1['token']

    response2 = requests.post(config.url + 'auth/register/v2', json={"email" : "user2@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    register_ret2 = response2.json()
    auid2 = register_ret2['auth_user_id']

    dm_create_response = requests.post(config.url + 'dm/create/v1', json={"token" : token1, "u_ids": [auid2]})
    dm_create_ret = dm_create_response.json()
    dm_id = dm_create_ret['dm_id']

    dict = {'token': token1, 'dm_id' : dm_id + 1}
    details_response = requests.get(config.url + 'dm/details/v1', params=dict)
    assert details_response.status_code == 400

# Tests that the dm_details function returns the same for all dm members, and that the correct info is returned
def test_dm_details_works():
    requests.delete(config.url + 'clear/v1')

    response1 = requests.post(config.url + 'auth/register/v2', json={"email" : "user1@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    register_ret1 = response1.json()
    token1 = register_ret1['token']
    auid1 = register_ret1['auth_user_id']

    response2 = requests.post(config.url + 'auth/register/v2', json={"email" : "user2@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    register_ret2 = response2.json()
    token2 = register_ret2['token']
    auid2 = register_ret2['auth_user_id']

    dm_create_response = requests.post(config.url + 'dm/create/v1', json={"token" : token1, "u_ids": [auid2]})
    dm_create_ret = dm_create_response.json()
    dm_id = dm_create_ret['dm_id']

    dict = {'token': token1, 'dm_id' : dm_id}
    dm_details_resp1 = requests.get(config.url + 'dm/details/v1', params=dict)
    assert dm_details_resp1.status_code == 200
    dm_details1 = dm_details_resp1.json()

    dict = {'token': token2, 'dm_id' : dm_id}
    dm_details_resp2 = requests.get(config.url + 'dm/details/v1', params=dict)
    assert dm_details_resp2.status_code == 200
    dm_details2 = dm_details_resp2.json()

    assert dm_details1 == dm_details2

    assert dm_details1 == {"name": "bobsmith, bobsmith0", 
                           "members": [{"u_id": auid1, "email": "user1@gmail.com", "name_first" : "Bob", "name_last" : "Smith", "handle_str": "bobsmith"},
                                       {"u_id": auid2, "email": "user2@gmail.com", "name_first" : "Bob", "name_last" : "Smith", "handle_str": "bobsmith0"}]}



# Test for an AccessError when an invalid token is given 
def test_dm_details_invalid_token():
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

    dict = {'token': token1+token2, 'dm_id' : dm_id}
    details_response = requests.get(config.url + 'dm/details/v1', params=dict)
    assert details_response.status_code == 403

# Tests for an AccessError when the dm_id belongs to a valid dm, but the authorised user is not a member of it
def test_dm_details_user_not_a_member_of_dm():
    requests.delete(config.url + 'clear/v1')

    response1 = requests.post(config.url + 'auth/register/v2', json={"email" : "user1@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    register_ret1 = response1.json()
    token1 = register_ret1['token']

    response2 = requests.post(config.url + 'auth/register/v2', json={"email" : "user2@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    register_ret2 = response2.json()
    auid2 = register_ret2['auth_user_id']

    dm_create_response = requests.post(config.url + 'dm/create/v1', json={"token" : token1, "u_ids": [auid2]})
    dm_create_ret = dm_create_response.json()
    dm_id = dm_create_ret['dm_id']

    response3 = requests.post(config.url + 'auth/register/v2', json={"email" : "user3@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    register_ret3 = response3.json()
    token3 = register_ret3['token']

    dict = {'token': token3, 'dm_id' : dm_id}
    details_response = requests.get(config.url + 'dm/details/v1', params=dict)
    assert details_response.status_code == 403