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

# Test that the dms are listed as expected
def test_dm_list_works():
    requests.delete(config.url + 'clear/v1')
    # Register 2 users
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "password", "name_first": "Mario", "name_last": "Kart"})
    return1 = response1.json()
    token1 = return1['token']

    response2 = requests.post(config.url + 'auth/register/v2', json = {"email": "def@gmail.com", "password": "password", "name_first": "Luigi", "name_last": "Kart"})
    return2 = response2.json()
    token2 = return2['token']
    auid2 = return2['auth_user_id']
    
    # Create a dm between the first two users
    dm_create_response1 = requests.post(config.url + 'dm/create/v1', json={"token": token1, "u_ids": [auid2]})
    dm_create_return1 = dm_create_response1.json()
    dm_id1 = dm_create_return1['dm_id']

    # Check that dm_list returns correctly for both users
    dm_list_response1 = requests.get(config.url + 'dm/list/v1', params={"token": token1})
    dm_list_ret1 = dm_list_response1.json()
    assert dm_list_ret1['dms'] == [{"dm_id": dm_id1, "name": "luigikart, mariokart"}]

    dm_list_response2 = requests.get(config.url + 'dm/list/v1', params={"token": token2})
    dm_list_ret2 = dm_list_response2.json()
    assert dm_list_ret2['dms'] == [{"dm_id": dm_id1, "name": "luigikart, mariokart"}]

    # Register a third user, and create a dm between them and user 1
    response3 = requests.post(config.url + 'auth/register/v2', json = {"email": "abcd@gmail.com", "password": "password", "name_first": "Peach", "name_last": "Kart"})
    return3 = response3.json()
    auid3 = return3['auth_user_id']
    token3 = return3['token']
    # (But first check that they aren't listed in any dms)
    dm_list_response3 = requests.get(config.url + 'dm/list/v1', params={"token": token3})
    dm_list_ret3 = dm_list_response3.json()
    assert dm_list_ret3['dms'] == []

    dm_create_response2 = requests.post(config.url + 'dm/create/v1', json={"token": token1, "u_ids": [auid3]})
    dm_create_return2 = dm_create_response2.json()
    dm_id2 = dm_create_return2['dm_id']

    # Check that user 1 is listed in both dms
    dm_list_response4 = requests.get(config.url + 'dm/list/v1', params={"token": token1})
    dm_list_ret4 = dm_list_response4.json()
    assert dm_list_ret4['dms'] == [{"dm_id": dm_id1, "name": "luigikart, mariokart"}, {"dm_id": dm_id2, "name": "mariokart, peachkart"}]


# Test that an AccessError is raised when an invalid token is given
def test_invalid_token():
    requests.delete(config.url + 'clear/v1')
    # Register a user and create an invalid jwt from it
    response = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "password", "name_first": "Mario", "name_last": "Kart"})
    reg_return = response.json()
    token = reg_return['token']
    invalid_token = token + '33m8x13she18'
    
    # Check that an AccessError is thrown
    dm_list_response = requests.get(config.url + 'dm/list/v1', params={"token": invalid_token})
    assert dm_list_response.status_code == 403
