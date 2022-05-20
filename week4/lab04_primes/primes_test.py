from primes import factors
def test_prime_small_num():
    assert factors(3) == [3]
    
def test_prime_middle_num():
    assert factors(16) == [2, 2, 2, 2]

def test_prime_large_num():
    assert factors(21) == [3, 7]

def test_prime_superlarge_num():
    assert factors(650) == [2, 5, 5, 13]
