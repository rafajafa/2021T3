Assumption 1: Order of members lists
    The all_members and owner_members lists in the data_store must contain the users in the order they were added.

Assumption 2: General
    All input is of the correct type, e.g. the argument 'auth_user_id' will always be an integer.

Assumption 3: Theoretical length of input strings
    The password can be of any length above 6 characters. The email can be of any length. The handle string can be of zero length if name_first and name_last only contain non-alphanumeric characters. 

Assumption 4: Email validity checking
    The re.match module is used to check the email regex, rather than the re.fullmatch module, in auth_register_v1. This was approved of on the forum, since we ran into problems using re.fullmatch. However this implies the assumption that if the email argument passed to auth_register_v1 has the form of a valid email string joined to the beginning of another string containing some other invalid characters, then the email may still be accepted (re.match only ensures that the beginning of the string matches the regex, whereas re.fullmatch ensures the entire string is of the correct regex format).

Assumption 5: Channel_messages start index
    We assume the value for the start value in channel_messages function is always positive or zero.

Assumption 6: Channel names
    Multiple channels can share the same name. Justifiable since they are distinguishable by their channel_id.

Assumption 7: Data_store element 'channels'
    Channels list in the data_store conatins the messages

Assumption 8: Data_store structure
    Data_store will store two lists, users and channels
