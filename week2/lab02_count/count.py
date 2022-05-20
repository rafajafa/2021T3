def count_char(message):
    '''
    Counts the number of occurrences of each character in a string. The result should be a dictionary where the key is the character and the dictionary is its count.

    For example,
    >>> count_char("HelloOo!")
    {'H': 1, 'e': 1, 'l': 2, 'o': 2, 'O': 1, '!': 1}
    '''
    dict_freq = {}
    for i in message:
        if i in dict_freq:
            dict_freq[i] += 1
        else:
            dict_freq[i] = 1
    return dict_freq

if __name__ == '__main__':
    print(count_char("abc"))