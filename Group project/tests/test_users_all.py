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

def test_users_all_invalid_token(setup, token):
	response = requests.get(config.url + 'users/all/v1?token=' + token + 'wrong')
	assert response.status_code == 403

def test_valid_users_all(setup):
	response = requests.post(config.url + 'auth/register/v2', json = {"email" : "user1@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last" : "Smith"})
	auid_dict = response.json()
	token = auid_dict['token']
	uid = auid_dict['auth_user_id']
	response = requests.get(config.url + 'users/all/v1?token=' + token)
	user_dict = response.json()
	user_list = user_dict['users']
	assert user_list == [{"u_id" : uid, "email" : "user1@gmail.com", "name_first" : "Bob", "name_last" : "Smith", "handle_str" : "bobsmith"}]