import requests
import pytest
from src import config
from src.other import clear_v1
from src.helpers import generate_id, generate_message_id

def test_generate_id():
    clear_v1()
    ret = generate_id()
    ret2 = generate_id()
    assert ret == 1 and ret2 == 2

def test_generate_message_id():
    clear_v1()
    ret = generate_message_id()
    ret2 = generate_message_id()
    assert ret == 1 and ret2 == 2
