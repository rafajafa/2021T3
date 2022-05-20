'''
Tests for check_password()
'''
from password import check_password

def test_hor_password():
    p = "123456"
    str = check_password(p)
    assert str == "Horrible password"

def test_hor_password2():
    p = "password"
    str = check_password(p)
    assert str == "Horrible password"

def test_poor_password():
    p = "1234567"
    str = check_password(p)
    assert str == "Poor password"

def test_mod_password():
    p = "abcdefgh123"
    str = check_password(p)
    assert str == "Moderate password"

def test_strong_password():
    p = "Orangeisawesome123"
    str = check_password(p)
    assert str == "Strong password"