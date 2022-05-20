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

# A fixture to register a user and create a channel for them
@pytest.fixture
def token():
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "stonk", "name_last": "mcstonker"})
    resp = response.json()
    token = resp['token']
    return token

@pytest.fixture
def cid(token):
    channel_response = requests.post(config.url + 'channels/create/v2', json = {"token": token, "name": "channel1", "is_public": False})
    channel_return = channel_response.json()
    cid = channel_return['channel_id']
    return cid

# Test that an AccessError is raised when an invalid token is given (invalid due to conclusion of the session)
def test_invalid_token(token, cid):
    logo = requests.post(config.url + 'auth/logout/v1', json = {"token": token})
    print(logo.status_code)

    message_response = requests.post(config.url + 'message/send/v1', json = {"token": token, "channel_id": cid, "message": "Hello World"})
    assert message_response.status_code == 403

# Test that an InputError is raised when the channel_id of a non-existent channel is given
def test_invalid_channel_id(token, cid):
    message_response = requests.post(config.url + 'message/send/v1', json = {"token": token, "channel_id": cid+1, "message": "Hello World"})
    assert message_response.status_code == 400

# Test that an InputError is raised when the message is not of the correct length range
def test_message_length(token, cid):
    # If the message is too long (> 1000 chars)
    long_message = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

    message_response = requests.post(config.url + 'message/send/v1', json = {"token": token, "channel_id": cid, "message": long_message})
    assert message_response.status_code == 400
    # If the message is 0 chars long
    message_response = requests.post(config.url + 'message/send/v1', json = {"token": token, "channel_id": cid, "message": ""})
    assert message_response.status_code == 400

# Test that an AccessError is thrown when the channel_id is valid and the authorised user is not a member of the channel
def test_non_member_user():
    requests.delete(config.url + 'clear/v1')
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "stonk", "name_last": "mcstonker"})
    resp1 = response1.json()
    token1 = resp1['token']

    channel_response = requests.post(config.url + 'channels/create/v2', json = {"token": token1, "name": "channel1", "is_public": False})
    channel_return = channel_response.json()
    cid = channel_return['channel_id']

    response2 = requests.post(config.url + 'auth/register/v2', json = {"email": "abcd@gmail.com", "password": "thepassword", "name_first": "stonk", "name_last": "mcstonker"})
    resp2 = response2.json()
    token2 = resp2['token']

    message_response = requests.post(config.url + 'message/send/v1', json = {"token": token2, "channel_id": cid, "message": "Hello!"})
    assert message_response.status_code == 403

# Test that an AccessError is thrown when the channel_id is valid and the sender is not registered
def test_unregistered_sender(token, cid):
    invalid_token = token + '123dkef312k'

    message_response = requests.post(config.url + 'message/send/v1', json = {"token": invalid_token, "channel_id": cid, "message": "Hello World"})
    assert message_response.status_code == 403


# Tests if an AccessError is thrown when both Input and Access Errors apply
# Specifically, if a non-member is attempting to send a message with length outside the valid length range
def test_non_member_zero_length_msg():
    requests.delete(config.url + 'clear/v1')
    response1 = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "stonk", "name_last": "mcstonker"})
    resp1 = response1.json()
    token1 = resp1['token']

    channel_response = requests.post(config.url + 'channels/create/v2', json = {"token": token1, "name": "channel1", "is_public": False})
    channel_return = channel_response.json()
    cid = channel_return['channel_id']

    response2 = requests.post(config.url + 'auth/register/v2', json = {"email": "abcd@gmail.com", "password": "thepassword", "name_first": "stonk", "name_last": "mcstonker"})
    resp2 = response2.json()
    token2 = resp2['token']

    message_response = requests.post(config.url + 'message/send/v1', json = {"token": token2, "channel_id": cid, "message": ""})
    assert message_response.status_code == 403


def test_different_message_ids():
    # Test if the message ids are different in the same channel
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'auth/register/v2', json = {"email": "abc@gmail.com", "password": "thepassword", "name_first": "stonk", "name_last": "mcstonker"})
    resp = response.json()
    token = resp['token']

    channel_response1 = requests.post(config.url + 'channels/create/v2', json = {"token": token, "name": "channel1", "is_public": False})
    channel_return1 = channel_response1.json()
    cid1 = channel_return1['channel_id']

    message_response1 = requests.post(config.url + 'message/send/v1', json = {"token": token, "channel_id": cid1, "message": "Hello"})
    assert message_response1.status_code == 200
    message_return1 = message_response1.json()
    msg_id1 = message_return1['message_id']

    message_response2 = requests.post(config.url + 'message/send/v1', json = {"token": token, "channel_id": cid1, "message": "World"})
    assert message_response2.status_code == 200
    message_return2 = message_response2.json()
    msg_id2 = message_return2['message_id']

    assert msg_id1 != msg_id2
    # Test if the message ids are different in different channels
    channel_response2 = requests.post(config.url + 'channels/create/v2', json = {"token": token, "name": "channel2", "is_public": False})
    channel_return2 = channel_response2.json()
    cid2 = channel_return2['channel_id']

    message_response3 = requests.post(config.url + 'message/send/v1', json = {"token": token, "channel_id": cid2, "message": "Tempest"})
    assert message_response3.status_code == 200
    message_return3 = message_response3.json()
    msg_id3 = message_return3['message_id']

    assert msg_id1 != msg_id3
    assert msg_id2 != msg_id3
