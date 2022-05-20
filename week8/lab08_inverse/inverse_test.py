from inverse import inverse
from hypothesis import given, Verbosity, strategies, settings
from hypothesis.strategies import dictionaries, integers, text

@given(dictionaries(integers(min_value=0, max_value=5), integers(min_value=0, max_value=5), min_size = 1, max_size = 4))
@settings(verbosity = Verbosity.verbose)
def test_reverse(dict):
    new_dict = inverse(dict)
    print(new_dict)
    #assert False
    
@given(dictionaries(integers(min_value=0, max_value=5), text(alphabet = "abcdefg", min_size=1, max_size=5), min_size = 1, max_size = 5))
@settings(verbosity = Verbosity.verbose)
def test_reverse_with_string(dict):
    new_dict = inverse(dict)
    print(new_dict)
    #assert False


def test_reverse_simple():
    dict = inverse({2: 'ball', 10: 'football'})
    assert dict == {'ball': [2], 'football' : [10]}

def test_reverse_num_and_string():
    dict = inverse({1: 'A', 2: 'B', 3: 'A'})
    assert dict == {'A': [1, 3], 'B': [2]}

def test_reverse_string():
    dict = inverse({'1': 'A', '2': 'B', '3': 'A'})
    assert dict == {'A': ['1', '3'], 'B': ['2']}
