from typing import Union, Optional

def multiply_by_two(number: int) -> int:
    '''
    Multiplies a given number by two.
    '''
    return number * 2

def print_message(message: str) -> str:
    '''
    Prints a given message.
    '''
    print(message)

def sum_list_of_numbers(numbers) -> int:
    '''
    Returns the sum of a list of numbers
    '''
    if numbers == []:
        return 0
    return sum(numbers)

def sum_iterable_of_numbers(numbers) -> int:
    '''
    Calculates the sum of an iterable of numbers

    numbers: any iterable

    Return value: integer
    '''
    return sum(numbers)

def is_in(needle: Union[str, int], haystack) -> bool:
    '''
    Checks if the given item is in a list

    Parameters:
    - needle: a string or an integer
    - haystack: a list of strings or integers

    Return value: bool - if the needle is in the haystack
    '''
    if needle in haystack:
        return True
    else:
        return False

def index_of_number(item: int, numbers) -> Union[int, None]:
    '''
    Returns the index of the given item in a list of numbers

    Parameters:
    - item: an integer
    - numbers: a list of numbers

    Return value: the index of the item, or None if the items is not in numbers
    '''
    for idx, number in enumerate(numbers):
        if item == number:
            return idx
    return None
