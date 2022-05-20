'''
Tests for reverse_words()
'''
import pytest
from reverse import reverse_words

def test_example():
    assert reverse_words(["Hello World", "I am here"]) == ['World Hello', 'here am I']

def test_1():
    l = ["test1 is awesome", "is this working"]
    l = reverse_words(l)
    assert l == ["awesome is test1", "working this is"]

def test_three():
    l = ["test1 is awesome", "is this working", "but is it"]
    l = reverse_words(l)
    assert l == ["awesome is test1", "working this is", "it is but"]

def test_tuple_num():
    l = ["1 2 3", "4 5 6"]
    l = reverse_words(l)
    assert l == ["3 2 1", "6 5 4"]

def test_three_num():
    l = ["1 2 3", "4 5 6", "7 8 9"]
    l = reverse_words(l)
    assert l == ["3 2 1", "6 5 4", "9 8 7"]

def test_5():
    l = ["hello world"]
    l = reverse_words(l)
    assert l == ["world hello"]