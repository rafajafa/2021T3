from list_exercises import reverse_list, minimum, sum_list

def test_reverse():
    l = ["how", "are", "you"]
    reverse_list(l)
    assert l == ["you", "are", "how"]

def test_reverse_1():
    l = ["hello", "world", "!"]
    reverse_list(l)
    assert l == ["!", "world", "hello"]

def test_reverse_2():
    l = ["test", "reverse", "2"]
    reverse_list(l)
    assert l == ["2", "reverse", "test"]

def test_min_positive():
    assert minimum([1, 2, 3, 10]) == 1

def test_min_positive_1():
    assert minimum([3,2,5,10]) == 2

def test_min_positive_2():
    assert minimum([3,10,5,6]) == 3

def test_sum_positive():
    assert sum_list([7, 7, 7]) == 21

def test_sum_positive_1():
    assert sum_list([7, 8, 9]) == 24

def test_sum_positive_2():
    assert sum_list([10, 10, 10]) == 30
