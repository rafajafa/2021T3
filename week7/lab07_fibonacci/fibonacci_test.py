from fibonacci import fib
def test_0():
    assert fib(0) == 0
def test_1():
    assert fib(1) == 1
def test_small_number():
    assert fib(7) == 13
def test_large_number():
    assert fib(20) == 6765
