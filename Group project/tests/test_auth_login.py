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

# If the email is not correct
def test_auth_login_email():
    # Test 1 - generic incorrect email
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json = {"email": "validemail@gmail.com", "password": "123abc!@#", "name_first": "first_name", "name_last": "last_name"})
    response = requests.post(config.url + 'auth/login/v2', json = {"email": "didntusethis@gmail.com", "password": "123abc!@#"})
    assert response.status_code == 400
    # Test 2 - space at the end of the email
    response1 = requests.post(config.url + 'auth/login/v2', json = {"email": "validemail@gmail.com ", "password": "123abc!@#"})
    assert response1.status_code == 400
    # Test 3 - missing character
    response2 = response1 = requests.post(config.url + 'auth/login/v2', json = {"email": "validemail@gmail.co", "password": "123abc!@#"})
    assert response2.status_code == 400

# If the email is correct but the password is not
def test_auth_login_password():
    # Test 1 - Generic incorrect password
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json = {"email": "validemail@gmail.com", "password": "123abc!@#", "name_first": "first_name", "name_last": "last_name"})
    response = requests.post(config.url + 'auth/login/v2', json = {"email": "validemail@gmail.com", "password": "123abcd!@#"})
    assert response.status_code == 400
    # Test 2 - space at the end of the password
    response1 = requests.post(config.url + 'auth/login/v2', json = {"email": "validemail@gmail.com", "password": "123abc!@# "})
    assert response1.status_code == 400
    # Test 3 - missing character
    response2 = requests.post(config.url + 'auth/login/v2', json = {"email": "validemail@gmail.com", "password": "123abc!@"})
    assert response2.status_code == 400

# If both the email and the password are incorrect
def test_auth_login_not_registered():
    # Test 1 - Generic incorrect details
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + 'auth/register/v2', json = {"email": "validemail@gmail.com", "password": "123abc!@#", "name_first": "first_name", "name_last": "last_name"})
    response = requests.post(config.url + 'auth/login/v2', json = {"email": "didntusethis@gmail.com", "password": "123abcd!@#"})
    assert response.status_code == 400
    # Test 2 - incorrect due to additional spaces
    response1 = requests.post(config.url + 'auth/login/v2', json = {"email": "validemail@ gmail.com", "password": "123 abc!@#"})
    assert response1.status_code == 400
    # Test 3 - missing characters
    response1 = requests.post(config.url + 'auth/login/v2', json = {"email": "validemail@gmail.co", "password": "123bc!@#"})
    assert response1.status_code == 400

# Use register to cross-check that the correct auth_user_id is being returned
def test_auth_login_works():
    requests.delete(config.url + 'clear/v1')
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "password", "name_first": "first_name", "name_last": "last_name"})
    resp1 = response1.json()
    auid1 = resp1['auth_user_id']

    response2 = requests.post(config.url + 'auth/login/v2', json = {"email": "abc@gmail.com", "password": "password"})
    resp2 = response2.json()
    auid2 = resp2['auth_user_id']
    assert auid1 == auid2



