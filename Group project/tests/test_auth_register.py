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


def test_auth_register_invalid_email():
    requests.delete(config.url + "clear/v1")
    # Test 1 - missing @ and .com
    response = requests.post(config.url + "auth/register/v2", json={"email": "abc", "password": "password", "name_first": "first_name", "name_last": "last_name"})
    assert response.status_code == 400
    # Test 2 - no email
    response = requests.post(config.url + "auth/register/v2", json={"email": "", "password": "password", "name_first": "first_name", "name_last": "last_name"})
    assert response.status_code == 400
    # Test 3 - no @
    response = requests.post(config.url + "auth/register/v2", json={"email": "abcgmail.com", "password": "password", "name_first": "first_name", "name_last": "last_name"})
    assert response.status_code == 400
    # Test 4 - no .com
    response = requests.post(config.url + "auth/register/v2", json={"email": "abc@gmail", "password": "password", "name_first": "first_name", "name_last": "last_name"})
    assert response.status_code == 400

# A duplicate email should trigger an input error
def test_auth_register_duplicate_email():
    requests.delete(config.url + "clear/v1")
    # Test 1 - Same details
    requests.post(config.url + "auth/register/v2", json = {"email": "abc@gmail.com", "password": "password", "name_first": "first_name", "name_last": "last_name"})
    resp1 = requests.post(config.url + "auth/register/v2", json = {"email": "abc@gmail.com", "password": "password", "name_first": "first_name", "name_last": "last_name"})
    assert resp1.status_code == 400
    # Test 2 - different details
    requests.post(config.url + "auth/register/v2", json = {"email": "def@gmail.com", "password": "password", "name_first": "first_name", "name_last": "last_name"})
    resp2 = requests.post(config.url + "auth/register/v2", json = {"email": "def@gmail.com", "password": "password1", "name_first": "first_name1", "name_last": "last_name1"})
    assert resp2.status_code == 400

# The name_first must be between 1 and 50 characters long
def test_auth_register_firstname_length():
    requests.delete(config.url + "clear/v1")
    # Test 1 - name_first is too short
    resp1 = requests.post(config.url + "auth/register/v2", json = {"email": "abc@gmail.com", "password": "password", "name_first": "", "name_last": "last_name"})
    assert resp1.status_code == 400
    # Test 2 - name_first is too long
    resp2 = requests.post(config.url + "auth/register/v2", json = {"email": "def@gmail.com", "password": "password", "name_first": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "name_last": "last_name"})
    assert resp2.status_code == 400
    
# The name_first must be between 1 and 50 characters long
def test_auth_register_lastname_length():
    requests.delete(config.url + 'clear/v1')
    # Test 1 - name_first is too short
    resp1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "password", "name_first": "first_name", "name_last": ""})
    assert resp1.status_code == 400
    # Test 2 - name_first is too long
    resp2 = requests.post(config.url + 'auth/register/v2', json = {"email": "def@gmail.com", "password": "password", "name_first": "first_name", "name_last": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"})
    assert resp2.status_code == 400

# The password must be at least 6 characters in length
def test_auth_register_password_length():
    requests.delete(config.url + 'clear/v1')
    # Test 1 - len(password) < 6
    resp1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "pass", "name_first": "first_name", "name_last": "last_name"})
    assert resp1.status_code == 400
    # Test 2 - no password
    resp2 = requests.post(config.url + 'auth/register/v2', json = {"email": "def@gmail.com", "password": "", "name_first": "first_name", "name_last": "last_name"})
    assert resp2.status_code == 400

# Testing if auth_register returned a viable auth_user_id
def test_auth_register_return():
    requests.delete(config.url + 'clear/v1')
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "password", "name_first": "first_name", "name_last": "last_name"})
    resp1 = response1.json()
    auid1 = resp1['auth_user_id']

    response2 = requests.post(config.url + 'auth/login/v2', json = {"email": "abc@gmail.com", "password": "password"})
    resp2 = response2.json()
    auid2 = resp2['auth_user_id']
    assert auid1 == auid2

# Test to ensure that when two different people register, they receive two different auth_user_id's
def test_auth_register_diff_id():
    requests.delete(config.url + 'clear/v1')
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "first_name", "name_last": "last_name"})
    resp1 = response1.json()
    auid1 = resp1['auth_user_id']

    response2 = requests.post(config.url + 'auth/register/v2', json = {"email": "def@gmail.com", "password": "thepassword123", "name_first": "first_name", "name_last": "last_name"})
    resp2 = response2.json()
    auid2 = resp2['auth_user_id']

    assert auid1 != auid2

def test_auth_register_handle_return():
    # Test 1 - generic
    requests.delete(config.url + 'clear/v1')
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "stonk", "name_last": "mcstonker"})
    resp1 = response1.json()
    token = resp1['token']
    ch_resp = requests.post(config.url + 'channels/create/v2', json = {"token": token, "name": "channel1", "is_public": False})
    ch_ret = ch_resp.json()
    cid = ch_ret['channel_id']

    dict = {'token' : token, 'channel_id' : cid}
    details_resp = requests.get(config.url + 'channel/details/v2', params=dict)
    details_ret = details_resp.json()
    own_mem = details_ret['owner_members']
    owner = own_mem[0]
    handle = owner['handle_str']
    assert handle == 'stonkmcstonker'

    # Test 2 - more than 20 chars
    requests.delete(config.url + 'clear/v1')
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "stonksonite", "name_last": "mcstonkerson"})
    resp1 = response1.json()
    token = resp1['token']
    ch_resp = requests.post(config.url + 'channels/create/v2', json = {"token": token, "name": "channel1", "is_public": False})
    ch_ret = ch_resp.json()
    cid = ch_ret['channel_id']
    details_resp = requests.get(config.url + 'channel/details/v2', params=dict)
    details_ret = details_resp.json()
    own_mem = details_ret['owner_members']
    owner = own_mem[0]
    handle = owner['handle_str']
    assert handle == 'stonksonitemcstonker'

    # Test 3 - Uppercase chars
    requests.delete(config.url + 'clear/v1')
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "Stonk", "name_last": "McStonker"})
    resp1 = response1.json()
    token = resp1['token']
    ch_resp = requests.post(config.url + 'channels/create/v2', json = {"token": token, "name": "channel1", "is_public": False})
    ch_ret = ch_resp.json()
    cid = ch_ret['channel_id']
    details_resp = requests.get(config.url + 'channel/details/v2', params=dict)
    details_ret = details_resp.json()
    own_mem = details_ret['owner_members']
    owner = own_mem[0]
    handle = owner['handle_str']
    assert handle == 'stonkmcstonker'

    # Test 4 - numbers
    requests.delete(config.url + 'clear/v1')
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "5t0nk", "name_last": "mc5t0nk3r"})
    resp1 = response1.json()
    token = resp1['token']
    ch_resp = requests.post(config.url + 'channels/create/v2', json = {"token": token, "name": "channel1", "is_public": False})
    ch_ret = ch_resp.json()
    cid = ch_ret['channel_id']
    details_resp = requests.get(config.url + 'channel/details/v2', params=dict)
    details_ret = details_resp.json()
    own_mem = details_ret['owner_members']
    owner = own_mem[0]
    handle = owner['handle_str']
    assert handle == '5t0nkmc5t0nk3r'

    # Test 5 - numbers, uppercase, overflow
    requests.delete(config.url + 'clear/v1')
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "ST0nK50niTe", "name_last": "mc5T0nK3r50n"})
    resp1 = response1.json()
    token = resp1['token']
    ch_resp = requests.post(config.url + 'channels/create/v2', json = {"token": token, "name": "channel1", "is_public": False})
    ch_ret = ch_resp.json()
    cid = ch_ret['channel_id']
    details_resp = requests.get(config.url + 'channel/details/v2', params=dict)
    details_ret = details_resp.json()
    own_mem = details_ret['owner_members']
    owner = own_mem[0]
    handle = owner['handle_str']
    assert handle == 'st0nk50nitemc5t0nk3r'

# Test that two people with the same first/last names receive different handles in accordance with the spec
def test_auth_register_diff_handle():
    # Test 1
    requests.delete(config.url + 'clear/v1')
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "testhandle", "name_last": "thelastname"})
    resp1 = response1.json()
    token1 = resp1['token']
    ch_resp1 = requests.post(config.url + 'channels/create/v2', json = {"token": token1, "name": "channel1", "is_public": False})
    ch_ret1 = ch_resp1.json()
    cid1 = ch_ret1['channel_id']
    dict = {'token' : token1, 'channel_id' : cid1}
    details_resp1 = requests.get(config.url + 'channel/details/v2', params=dict)
    details_ret1 = details_resp1.json()
    own_mem1 = details_ret1['owner_members']
    owner1 = own_mem1[0]
    handle1 = owner1['handle_str']

    response2 = requests.post(config.url + 'auth/register/v2', json = {"email": "def@gmail.com", "password": "thepassword1", "name_first": "testhandle", "name_last": "thelastname"})
    resp2 = response2.json()
    token2 = resp2['token']
    ch_resp2 = requests.post(config.url + 'channels/create/v2', json = {"token": token2, "name": "channel2", "is_public": False})
    ch_ret2 = ch_resp2.json()
    cid2 = ch_ret2['channel_id']
    dict = {'token' : token2, 'channel_id' : cid2}
    details_resp2 = requests.get(config.url + 'channel/details/v2', params=dict)
    details_ret2 = details_resp2.json()
    own_mem2 = details_ret2['owner_members']
    owner2 = own_mem2[0]
    handle2 = owner2['handle_str']

    response3 = requests.post(config.url + 'auth/register/v2', json = {"email": "ghi@gmail.com", "password": "thepassword2", "name_first": "testhandle", "name_last": "thelastname"})
    resp3 = response3.json()
    token3 = resp3['token']
    ch_resp3 = requests.post(config.url + 'channels/create/v2', json = {"token": token3, "name": "channel3", "is_public": False})
    ch_ret3 = ch_resp3.json()
    cid3 = ch_ret3['channel_id']
    dict = {'token' : token3, 'channel_id' : cid3}
    details_resp3 = requests.get(config.url + 'channel/details/v2', params=dict)
    details_ret3 = details_resp3.json()
    own_mem3 = details_ret3['owner_members']
    owner3 = own_mem3[0]
    handle3 = owner3['handle_str']

    assert handle2 == handle1 + str(0)
    assert handle3 == handle1 + str(1)
