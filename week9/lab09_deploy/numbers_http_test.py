import pytest
import requests 

config = "http://localhost:5000/"

def test_multiply_by_two_http():
    dict = {'num' : 2}
    response = requests.get(config + '/multiply_by_two', params=dict)
    ret_dict = response.json()
    ret = ret_dict['ret']
    assert ret == 4

def test_print_message_http():
    dict = {'string' : 'COMP1531 is legit my favourite course ever'}
    response = requests.get(config + '/print_message', params=dict)
    assert response.status_code == 200

def test_sum_list_of_numbers_http():
    dict = {'list' : '1,2,3,4'}
    response = requests.get(config + '/sum_list_of_numbers', params=dict)
    ret_dict = response.json()
    ret = ret_dict['ret']
    assert ret == 10

'''
def test_sum_iterable_of_numbers_http():
    dict = {'list' : '1,10,100,1000'}
    response = requests.get(config + '/sum_iterable_of_numbers', params=dict)
    ret_dict = response.json()
    ret = ret_dict['ret']
    assert ret == 1111
'''
def test_is_in_http():
    dict = {'needle' : 1, 'haystack' : '1,2,3,4'}