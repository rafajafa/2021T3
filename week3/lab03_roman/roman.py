def roman(numerals):
    '''
    Given Roman numerals as a string, return their value as an integer. You may
    assume the Roman numerals are in the "standard" form, i.e. any digits
    involving 4 and 9 will always appear in the subtractive form.

    For example:
    >>> roman("II")
    2
    >>> roman("IV")
    4
    >>> roman("IX")
    9
    >>> roman("XIX")
    19
    >>> roman("XX")
    20
    >>> roman("MDCCLXXVI")
    1776
    >>> roman("MMXIX")
    2019
    '''
    roman_symbol = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000,'IV':4,'IX':9,'XL':40,'XC':90,'CD':400,'CM':900}
    char_index = 0
    num = 0
    while char_index < len(numerals):
        if char_index + 1 < len(numerals) and numerals[char_index:char_index+2] in roman_symbol:
            num += roman_symbol[numerals[char_index:char_index+2]]
            char_index += 2
        else:
            num += roman_symbol[numerals[char_index]]
            char_index += 1
    return num