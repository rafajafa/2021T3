import math

def factors(num):
    '''
    Returns a list containing the prime factors of 'num'. The primes should be
    listed in ascending order.

    For example:
    >>> factors(16)
    [2, 2, 2, 2]
    >>> factors(21)
    [3, 7]
    '''
    
    prime_list = []
    while num % 2 == 0:
        num = num / 2
        prime_list.append(2)
    for i in range(3, int(math.sqrt(num)+1), 2):
        while num % i == 0:
            prime_list.append(i)
            num = num / i
    if num > 2:
        prime_list.append(num)
    
    return sorted(prime_list)
        