from attr import dataclass
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


# Clear the data_store register a user and return their token
# TODO fix up the fixture and re-include the decorator
@pytest.fixture
def token():
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "password", "name_first": "first_name", "name_last": "last_name"})
    user_details = response.json()
    token = user_details['token']
    return token

# Tests various cases where the handle length is not acceptable
def test_sethandle_invalid_length(token):
    # Handle has no length
    resp = requests.put(config.url + 'user/profile/sethandle/v1', json = {"token": token, "handle_str": ""})
    assert resp.status_code == 400

    # Handle is too short
    resp = requests.put(config.url + 'user/profile/sethandle/v1', json = {"token": token, "handle_str": "ab"})
    assert resp.status_code == 400

    # Handle is too long
    resp = requests.put(config.url + 'user/profile/sethandle/v1', json = {"token": token, "handle_str": "abcdefghijklmnopqrstu"})
    assert resp.status_code == 400

def test_sethandle_non_alphanum_chars(token):
    # Handle contains non-alphanumeric chars
    resp = requests.put(config.url + 'user/profile/sethandle/v1', json = {"token": token, "handle_str": "acg#$@fd&454"})
    assert resp.status_code == 400

    # Handle is made of non-alphanumeric chars
    resp = requests.put(config.url + 'user/profile/sethandle/v1', json = {"token": token, "handle_str": "$@#^&*:!"})
    assert resp.status_code == 400

def test_handle_already_used(token):
    # Register someone with the handle_str already123used456
    requests.post(config.url + 'auth/register/v2', json = {"email": "abcd@gmail.com", "password": "password", "name_first": "already123", "name_last": "used456"})
    # Changing the handle to something thats already being used should return a status code of 400
    resp = requests.put(config.url + 'user/profile/sethandle/v1', json = {"token": token, "handle_str": "already123used456"})
    assert resp.status_code == 400

# Checks if the function works as it is meant to - i.e. a user can change their handle_str to a valid alternative 
def test_sethandle_works():
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'auth/register/v2', json = {"email": "abcd@gmail.com", "password": "password", "name_first": "first_name", "name_last": "last_name"})
    user_details = response.json()
    token = user_details['token']
    auid = user_details['auth_user_id']
    resp = requests.put(config.url + 'user/profile/sethandle/v1', json = {"token": token, "handle_str": "thisisok1234"})
    assert resp.status_code == 200

    dict = {'token' : token, 'u_id' : auid}
    response = requests.get(config.url + 'user/profile/v1', params=dict)
    profile_ret = response.json()
    user = profile_ret['user']
    new_handle_str = user['handle_str']
    assert new_handle_str == 'thisisok1234'

# Check edge cases for alternative handle lengths
def test_sethandle_works_edge_cases():
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'auth/register/v2', json = {"email": "abcd@gmail.com", "password": "password", "name_first": "first_name", "name_last": "last_name"})
    user_details = response.json()
    token = user_details['token']
    auid = user_details['auth_user_id']

    # 3-char handle_str
    resp = requests.put(config.url + 'user/profile/sethandle/v1', json = {"token": token, "handle_str": "yes"})
    assert resp.status_code == 200
    dict = {'token' : token, 'u_id' : auid}
    response = requests.get(config.url + 'user/profile/v1', params=dict)
    profile_ret = response.json()
    user = profile_ret['user']
    new_handle_str = user['handle_str']
    assert new_handle_str == 'yes'

    # 20-char handle_str
    resp = requests.put(config.url + 'user/profile/sethandle/v1', json = {"token": token, "handle_str": "abcdefghijklmnopqrst"})
    assert resp.status_code == 200

    response = requests.get(config.url + 'user/profile/v1', params=dict)
    profile_ret = response.json()
    user = profile_ret['user']
    new_handle_str = user['handle_str']
    assert new_handle_str == 'abcdefghijklmnopqrst'