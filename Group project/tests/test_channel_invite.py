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
    # create a user and return their token
    response = requests.post(config.url + 'auth/register/v2', json = {"email" : "user1@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last": "Smith"})
    auid_dict = response.json()
    token = auid_dict['token']
    return token

@pytest.fixture
def uid2():
    # create a second user and return their auth_user_id
    response = requests.post(config.url + 'auth/register/v2', json = {"email" : "user2@gmail.com", "password" : "Password123", "name_first" : "Bobby", "name_last": "Smithy"})
    auid_dict = response.json()
    uid2 = auid_dict['auth_user_id']
    return uid2

@pytest.fixture
def token3():
    # create a third user and return their token
    response = requests.post(config.url + 'auth/register/v2', json = {"email" : "user3@gmail.com", "password" : "Password123", "name_first" : "Bobbo", "name_last": "Smithy"})
    auid_dict = response.json()
    token3 = auid_dict['token']
    return token3

@pytest.fixture
def cid(token):
    # Create a channel
    channel_response = requests.post(config.url + 'channels/create/v2', json = {"token": token, "name": "channel1", "is_public": False})
    channel_return = channel_response.json()
    cid = channel_return['channel_id']
    return cid

# Test Channel invite succeeds
def test_channel_invite_success(setup, token, uid2, cid):
    # Invite second user to channel with owner's token
    channel_invite_response = requests.post(config.url + '/channel/invite/v2', json = {"token": token, "u_id": uid2, "channel_id": cid})
    # The user is successfully invited to channel
    assert channel_invite_response.status_code == 200

# Test when channel id is invalid.
def test_invalid_channel(setup, token, uid2, cid):
    # Pass in an invalid channel id
    check_channel_invalid_response = requests.post(config.url + 'channel/invite/v2', json = {"token": token, "channel_id": cid+1,"u_id": uid2})

    # Check for InputError
    assert check_channel_invalid_response.status_code == 400

# Test that the token is valid.
def test_invalid_token(setup, token, uid2, cid):
    # The inviter user does not exist.
    check_invalid_token_response = requests.post(config.url + 'channel/invite/v2', json = {"token": token + "wrong", "channel_id": cid,"u_id": uid2})
    # Check for AccessError
    assert check_invalid_token_response.status_code == 403

# Test u_id is valid.
def test_valid_invitee(setup, token, uid2, cid):
    # The invitee user does not exist.
    check_invalid_token_response = requests.post(config.url + 'channel/invite/v2', json = {"token": token, "channel_id": cid,"u_id": uid2 + 12345})
    # Check for InputError
    assert check_invalid_token_response.status_code == 400

# Test u_id is already channel member.
def test_user_is_already_member(setup, token, uid2, cid):
    # Invite the user into the channel
    requests.post(config.url + 'channel/invite/v2', json = {"token": token, "channel_id": cid,"u_id": uid2})
    # Invite the user into the channel, again
    check_user_is_member_response = requests.post(config.url + 'channel/invite/v2', json = {"token": token, "channel_id": cid,"u_id": uid2})
    # Check for InputError
    assert check_user_is_member_response.status_code == 400

# Test when the authorised user is not a member of the valid channel.
def test_valid_channel_user_not_owner(setup):
    # create a user and return their token
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email" : "user1@gmail.com", "password" : "Password123", "name_first" : "Bob", "name_last": "Smith"})
    auid_dict1 = response1.json()
    token1 = auid_dict1['token']
    uid1 = auid_dict1['auth_user_id']
    # create a second user and return their auth_user_id
    response2 = requests.post(config.url + 'auth/register/v2', json = {"email" : "user2@gmail.com", "password" : "Password123", "name_first" : "Bobby", "name_last": "Smithy"})
    auid_dict2 = response2.json()
    uid2 = auid_dict2['auth_user_id']
    # create a third user and get their auth_user_id and token
    response3 = requests.post(config.url + 'auth/register/v2', json = {"email" : "user3@gmail.com", "password" : "Password123", "name_first" : "Bobby", "name_last": "Smithy"})
    auid_dict3 = response3.json()
    token3 = auid_dict3['token']
    # Create a channel
    channel_response = requests.post(config.url + 'channels/create/v2', json = {"token": token1, "name": "channel1", "is_public": False})
    channel_return = channel_response.json()
    cid = channel_return['channel_id']
    # The third user attempts to invite the second user into the channel (neither of them being members)
    non_member_inviter_response1 = requests.post(config.url + 'channel/invite/v2', json = {"token": token3, "channel_id": cid, "u_id": uid2})
    assert non_member_inviter_response1.status_code == 403
    # The third user attempts to invite the first user into the channel
    # The third user is not a member, but the first one is - the AccessError resulting of the former not being a member should be raised instead of the InputError
    non_member_inviter_response2 = requests.post(config.url + 'channel/invite/v2', json = {"token": token3, "channel_id": cid, "u_id": uid1})
    assert non_member_inviter_response2.status_code == 403