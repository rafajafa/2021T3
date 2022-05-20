import math
def divisors(n):
  pass

# You may find this helpful
def is_prime(n):
    return n != 1 and divisors(n) == {1, n}

def factors(n):
    '''
    A function that generates the prime factors of n. For example
    >>> factors(12)
    [2,2,3]

    Params:
      n (int): The operand

    Returns:
      List (int): All the prime factors of n in ascending order.

    Raises:
      ValueError: When n is <= 1.
    '''
    if n <= 1:
      raise ValueError("value cannot be <=1 ")
    prime_list = []
    while n % 2 == 0:
        n = n / 2
        prime_list.append(2)
    for i in range(3, int(math.sqrt(n)+1), 2):
        while n % i == 0:
            prime_list.append(int(i))
            n = n / i
    if n > 2:
        prime_list.append(int(n))
    
    return sorted(prime_list)
