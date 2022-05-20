from prefix import prefix_search
import pytest

def test_documentation():
    assert prefix_search({"ac": 1, "ba": 2, "ab": 3}, "a") == { "ac": 1, "ab": 3}

def test_exact_match():
    assert prefix_search({"category": "math", "cat": "animal"}, "cat") == {"category": "math", "cat": "animal"}

# check for no match 
def test_no_match():
    with pytest.raises(KeyError):
        prefix_search({"category": "math", "cat": "animal"}, "abc")