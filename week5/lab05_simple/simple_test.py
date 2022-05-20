import pytest
import requests 
import json
from json import dumps
import server
from flask import Flask, request

config = "http://localhost:5000/"

@pytest.fixture
def clear_all():
    requests.delete(config + 'names/clear')

# Test if names are added successfully.
def test_names_added_success(clear_all):
    requests.post(config + 'names/add', json = {"name": "raf"})

    names_response1 = requests.get(config + 'names')
    names_response_json1 = names_response1.json()
    name = names_response_json1['name']
    assert name == ["raf"]
    
    requests.post(config + 'names/add', json = {'name': "Adam"})

    names_response2 = requests.get(config + 'names')
    names_response_json2 = names_response2.json()
    name2 = names_response_json2['name']
    assert name2 == ["raf", "Adam"]

# Test if names are removed 
def test_names_removed_success(clear_all):
    requests.post(config + 'names/add', json = {"name": "raf"})

    names_response1 = requests.get(config + 'names')
    names_response_json1 = names_response1.json()
    name = names_response_json1['name']
    assert name == ["raf"]

    requests.post(config + 'names/add', json = {'name': "Adam"})

    names_response2 = requests.get(config +'names')
    names_response_json2 = names_response2.json()
    name2 = names_response_json2['name']
    assert name2 == ["raf", "Adam"]

    requests.delete(config + 'names/remove', json = {'name': "Adam"})

    names_response3 = requests.get(config + 'names')
    names_response_json3 = names_response3.json()
    assert names_response_json3 == names_response_json1