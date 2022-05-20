from factors import factors, is_prime
from hypothesis import given, strategies
from hypothesis.strategies import integers, lists


@given(integers(min_value=2, max_value = 1000))
def test_random(num):
    prime_list = factors(num)
    print(prime_list, num)
    result = 1
    for x in prime_list:
        result = result * x
    assert result == num
    for i in prime_list:
        list = factors(i)
        assert len(list) == 1

def test_prime_small_num():
    assert factors(3) == [3]
    assert factors(2) == [2]
    
def test_prime_middle_num():
    assert factors(16) == [2, 2, 2, 2]

def test_prime_large_num():
    assert factors(21) == [3, 7]

def test_prime_superlarge_num():
    assert factors(650) == [2, 5, 5, 13]