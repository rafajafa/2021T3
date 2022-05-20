from count import count_char

def test_empty():
    assert count_char("") == {}

def test_simple():
    assert count_char("abc") == {"a": 1, "b": 1, "c": 1}

def test_double():
    assert count_char("aa") == {"a": 2}

def test_space():
    assert count_char(" ") == {" ": 1}

def test_Upper():
    assert count_char("Aa") == {"A": 1, "a": 1}

def test_num():
    assert count_char("Aa1") == {"A": 1, "a": 1, "1" :1}

def test_sen():
    assert count_char("This is") == {"T": 1, "h": 1, "i": 2, "s": 2, " ": 1}
