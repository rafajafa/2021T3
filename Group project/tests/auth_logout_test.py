import requests
import pytest
from src import config
from src.other import clear_v1

@pytest.fixture
def setup():
    requests.delete(config.url + 'clear/v1')

@pytest.fixture
def token():
    #create user1
    response = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "password", "name_first": "raf", "name_last": "woo"})
    #response = requests.post(config.url + 'auth/login/v2', json = {"email": "abc@gmail.com", "password": "password"})
    auid_dict = response.json()
    token = auid_dict['token']
    return token

def test_invalid_token(setup, token):
    wrong_token = token + 'wrong'
    response = requests.post(config.url + 'auth/logout/v1', json = {"token" : wrong_token})
    assert response.status_code == 403

def test_valid_auth_logout(setup, token):
    requests.post(config.url + 'auth/logout/v1', json = {"token" : token})
    response1 = requests.post(config.url + 'auth/logout/v1', json = {"token" : token})
    assert response1.status_code == 403
