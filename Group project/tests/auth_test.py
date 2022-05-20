import pytest

from src.auth import auth_login_v1, auth_register_v1
from src.error import InputError

#Test to ensure login is successful
def test_login_success():
    register_return = auth_register_v1('abc@gmail.com','password','raf','woo')
    auth_user_id1 = register_return['auth_user_id']
    login_return = auth_login_v1('abc@gmail.com', 'password')
    auth_user_id2 = login_return['auth_user_id']

    assert auth_user_id1 == auth_user_id2