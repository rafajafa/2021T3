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

def test_setemail_invalid_token(setup, token):
    response = requests.put(config.url + 'user/profile/setemail/v1', json = {"token" : token + "wrong", "email" : "user1@gmail.com"})
    assert response.status_code == 403

def test_setemail_invalid_email(setup, token):
    response = requests.put(config.url + 'user/profile/setemail/v1', json = {"token" : token, "email" : "abc"})
    assert response.status_code == 400
    response = requests.put(config.url + 'user/profile/setemail/v1', json = {"token" : token, "email" : "abcgmail.com"})
    assert response.status_code == 400
    response = requests.put(config.url + 'user/profile/setemail/v1', json = {"token" : token, "email" : ""})
    assert response.status_code == 400

def test_setemail_duplicate_email(setup, token):
    requests.post(config.url + 'auth/register/v2', json = {"email" : "user2@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
    response = requests.put(config.url + 'user/profile/setemail/v1', json = {"token" : token, "email" : "user2@gmail.com"})
    assert response.status_code == 400

def test_setemail_valid_email(setup, token):
    requests.put(config.url + 'user/profile/setemail/v1', json = {"token" : token, "email" : "changeuser1@gmail.com"})
    user_response = requests.get(config.url + 'users/all/v1?token=' + token)
    user_list = user_response.json()
    assert user_list == {"users" : [{"u_id" : 1, "email" : "changeuser1@gmail.com", "name_first" : "Bob", "name_last" : "Smith", "handle_str" : "bobsmith"}]}
