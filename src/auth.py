from src.data_store import data_store
from src.error import InputError, AccessError
import re
import hashlib
from src.helpers import generate_jwt, generate_id

email_regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"

def auth_login_v1(email, password):
    '''
    This function will login one user based on the email and password
    Argument: 
        email, type: string
        password, type: string

    Exceptions: 
        InputError: No such email found
        InputError: wrong password

    Return value:
        returns a dictionary with the auth_user_id associated with the given email and password, and a new token

    '''
    store = data_store.get()

    users = store['users']
    # if the user have type the correct password and email then return the auth_user_id
    # otherwise raise Input Error
    for user in users:
        if user['email'] == email:
            if hashlib.sha256(password.encode()).hexdigest() != user['password']:
                raise InputError
            else:
                auth_user_id = user['auth_user_id']

                # Add a new session_id to the user's sessions list
                new_session_id = generate_id()
                user['sessions'].append(new_session_id)

                # Save the datastore
                data_store.set(store)
                return {
                    'auth_user_id': auth_user_id,
                    'token': generate_jwt(auth_user_id, new_session_id)
                }
        
    raise InputError

def auth_register_v1(email, password, name_first, name_last):
    '''
    This function will register a user to the system
    Argument: 
        email, type: string
        password, type: string
        name_first, type: string
        name_last, type: string


    Exceptions: 
        InputError: same email found in the system
        InputError: email are in wrong format
        InputError: password is too short (less than 6 char)
        InputError: name_first too short or too long
        InputError: name_last too short or too long


    Return value:
        return a dictionary of auth_user_id of that new registered user
        (the auth_user_id for the new registered user will be the number 
        of total users in the system + 1), and a new jwt token

    '''
    store = data_store.get()

    # Test if email matches required regex/pattern
    if re.match(email_regex, email) == None:
        raise InputError
    
    #r''' will set it as raw string and avoid pylint error
    r'''
    if re.match('^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', email) == None:
        raise InputError
    '''
    
    # Test for duplicate email
    for user in store['users']:
        # the second element in a user tuple is the email - here we're checking if its the same as the input
        if user['email'] == email:
            raise InputError
    
    # Test for valid password must be geq to 6 chars in length
    if len(password) < 6:
        raise InputError

    # Test for a valid length in name_first
    if len(name_first) not in range(1, 51, 1):
        raise InputError

    # Test for a valid length in name_last
    if len(name_last) not in range(1, 51, 1):
        raise InputError

    # Generate an auth_user_id
    auth_user_id = len(store['users']) + 1

    # Generate a handle_str
    # Step 1: Join first and last names
    concat_str = str(name_first) + str(name_last)
    # Step 2: Convert to lowercase
    lower_str = concat_str.lower()
    # Step 3: Remove non-alphanumeric characters
    alphanum_str = ''.join(char for char in lower_str if char.isalnum())
    # Step 4: Compress the string 
    compressed_str = alphanum_str[0:20]
    # Step 5: Compare with existing handle_str's, and change if required
    append_int = 0 # This integer will be appended to the end of the handle_str if it macthes any other handles so far
    handle_str = compressed_str
    for user in store['users']:
        # If the handle_str matches that of another user
        if handle_str == user['handle_str']:
            # append the integer to the handle_str to make it distinct
            handle_str = compressed_str + str(append_int)
            # Iterate by 1 in case further matches are found
            append_int += 1

    # Generate the user's first session_id (using a helper function)
    first_session_id = generate_id()

    # If the user is the first to be registered thus far, they are a global owner; otherwise not
    is_global = False
    if auth_user_id == 1:
        is_global = True

    # Add information to the datastore
    store['users'].append({'auth_user_id': auth_user_id,
                            'email': email,
                            'password': hashlib.sha256(password.encode()).hexdigest(), 
                            'name_first': name_first, 
                            'name_last': name_last,
                            'handle_str': handle_str,
                            'sessions': [first_session_id],
                            'is_global' : is_global,
                            'is_removed': False
                            })
    # And save it
    data_store.set(store)

    return {
        'auth_user_id': auth_user_id,
        'token': generate_jwt(auth_user_id, first_session_id)
    }

def auth_logout_v1(auid, session_id):
    '''
    Logout
    Arguments:
        token - string
        session_id - int

    Exceptions:
        AccessError - if token not valid
        AccessError - if sessions is not valid

    Return Value:
        Returns nothing
    
    '''
    #invalid the token by removing the session_id in the user 
    store = data_store.get()
    users = store['users']
    user = next((item for item in users if item['auth_user_id'] == auid), None)
    if user is None:
        raise AccessError

    if any(item == session_id for item in user['sessions']):
        user['sessions'].remove(session_id)
    else:
        raise AccessError
