def reverse_words(string_list):
    '''
    Given a list of strings, return a new list where the order of the words is
    reversed
    '''
    new_string_list = []
    for i in string_list:
        words = i.split()
        words = list(reversed(words)) 
        words =  (" ".join(words))
        new_string_list += [words]
    
    return(new_string_list)

if __name__ == "__main__":
    print(reverse_words(["Hello World", "I am here"]))
    # it should print ['World Hello', 'here am I']
    print(reverse_words(["test1 is awesome", "is this working"]))

