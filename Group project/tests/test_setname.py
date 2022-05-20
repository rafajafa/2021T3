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

def test_invalid_firstname(setup, token):
    #Test1 - length of firstname less than 1
    response1 = requests.put(config.url + 'user/profile/setname/v1', json = {"token": token, "name_first": "", "name_last": "XIE"})
    assert response1.status_code == 400
    #Test2 - length of firstname more than 50
    response2 = requests.put(config.url + 'user/profile/setname/v1', json = {"token": token, "name_first": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "name_last": "XIE"})
    assert response2.status_code == 400

def test_invalid_lastname(setup, token):
    #Test1 - length of lastname less than 1
    response1 = requests.put(config.url + 'user/profile/setname/v1', json = {"token": token, "name_first": "James", "name_last": ""})
    assert response1.status_code == 400
    #Test2 - length of lastname more than 50
    response2 = requests.put(config.url + 'user/profile/setname/v1', json = {"token": token, "name_first": "James", "name_last": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"})
    assert response2.status_code == 400

def test_invalid_token(setup, token):
    response = requests.put(config.url + 'user/profile/setname/v1', json = {"token" : token + "wrong", "name_first": "Bobby", "name_last": "Smithy"})
    assert response.status_code == 403

def test_valid_setname(setup, token):
    requests.put(config.url + 'user/profile/setname/v1', json = {"token" : token, "name_first": "Bobby", "name_last": "Smithy"})
    user_list_response = requests.get(config.url + 'users/all/v1?token=' + token)
    user_list = user_list_response.json()
    assert user_list == {'users': [{'u_id': 1, 'email': 'user1@gmail.com', 'name_first': 'Bobby', 'name_last': 'Smithy', 'handle_str': 'bobsmith'}]}