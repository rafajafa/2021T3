import re
from json import dumps
from src.data_store import data_store
from src.error import InputError
from src.error import AccessError
from src.helpers import decode_jwt, token_is_valid
from src.auth import email_regex

def users_all(token):
    '''
    Returns a list of every user
    Arguments:
        token - string

    Exceptions:
        AccessError - if token not valid

    Return Value:
        Returns a list of the users
    
    '''
    store = data_store.get()
    users = store['users']

    user_dict = {
        'users' : []
    }

    for idx, user in enumerate(users):
        uid = users[idx]['auth_user_id']
        user_data = {'u_id' : uid}
        user_data.update({k:v for (k,v) in user.items() if (k != 'password' and k != 'is_global' and k != 'auth_user_id' and k != 'sessions' and k != 'is_removed')})
        user_dict['users'].append(user_data)

    return user_dict

def user_profile_v1(token, auth_user_id):
    '''
    return a user_profile
    Arguments:
        token - string
        auth_user_id - int

    Exceptions:
        AccessError - if token not valid
        InputError - if auth_user_id dont dont match any user

    Return Value:
        Returns the user's id, email, first and last name and handle string
    
    '''
    store = data_store.get()
    users = store['users']

    # if wrong token
    if not token_is_valid(token):
        raise AccessError("Invalid Token")

    user = next((item for item in users if item['auth_user_id'] == auth_user_id), None)
    # if no such user in users 
    if user is None:
        raise InputError("Invalid auth_user_id")
    
    profile_dict = {'u_id': auth_user_id,
                    'email': user['email'],
                    'name_first': user['name_first'],
                    'name_last' : user['name_last'],
                    'handle_str': user['handle_str']}
    
    return profile_dict


def user_profile_set_email(token, email):
    '''
    This function will change/set the email of the specified user
    Argument: 
        token, type: string
        email, type: string

    Exceptions: 
        AccessError: invalid or expired token
        InputError: the email is not a valid email
        InputError: the email is a duplicate email

    Return value:
        Returns an empty dictionary
    '''
    store = data_store.get()
    users = store['users']

    decoded_token = decode_jwt(token)
    auth_user_id = decoded_token['auth_user_id']

    if re.match(email_regex, email) == None:
	    raise InputError
		
	# Test for duplicate email
    for user in store['users']:
        # the second element in a user tuple is the email - here we're checking if its the same as the input
	    if user['email'] == email:
	        if user['auth_user_id'] != auth_user_id and user['is_removed'] == False:
	            raise InputError

    # The user whose email we want to change
    target_user = next((item for item in users if item['auth_user_id'] == auth_user_id), None)
    # The emailr is valid, so we can change it
    target_user['email'] = email
    return dumps({})

def user_set_handle_v1(token, handle_str):
    '''
    This function will change/set the handle_str of the specified user
    Argument: 
        token, type: string
        handle_str, type: string

    Exceptions: 
        AccessError: invalid or expired token
        InputError: the new handle_str is less than 3 or more than 20 characters long
        InputError: The handle_str contains non-alphanumeric characters
        InputError: If the handle_str is already being used by a non-removed user

    Return value:
        Returns an empty dictionary
    '''
    # Get the datastore
    store = data_store.get()
    users = store['users']

    # If the token does not belong to a registered user or is from an expired session
    if not token_is_valid(token):
        raise AccessError('Invalid Token')
    
    # Obtain the authorised user's auth_user_id
    decoded_token = decode_jwt(token)
    auth_user_id = decoded_token['auth_user_id']

    # If the new handle_str is not in the correct lentgh range
    if len(handle_str) not in range(3,21):
        raise InputError
    
    # If the new handle_str contains any non-alphanumeric characters
    if not handle_str.isalnum():
        raise InputError

    # If the new handle_str is being used by another user (not the user who requested the change)
    for user in users:
        if user['handle_str'] == handle_str:
            if user['auth_user_id'] != auth_user_id and user['is_removed'] == False:
                raise InputError

    # The user whose handle_str we want to change
    target_user = next((item for item in users if item['auth_user_id'] == auth_user_id), None)

    # The handle_str is valid, so we can change it
    target_user['handle_str'] = handle_str

    # Save the datastore
    data_store.set(store)

    return {}

def user_profile_set_name(token, name_first, name_last):
    '''
    This function will change/set the first name and last name of the specified user
    Argument: 
        token, type: string
        name_first, type: string
        name_last, type: string

    Exceptions: 
        AccessError: invalid or expired token
        InputError: the first name is less than 1 or more than 50 characters long
        InputError: the last name is less than 1 or more than 50 characters long

    Return value:
        Returns an empty dictionary
    '''
    store = data_store.get()
    users = store['users']

    if not token_is_valid(token):
        raise AccessError

    decoded_token = decode_jwt(token)
    auth_user_id = decoded_token['auth_user_id']

    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError

    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError

    target_user = next((item for item in users if item['auth_user_id'] == auth_user_id), None)
    target_user['name_first'] = name_first
    target_user['name_last'] = name_last

    data_store.set(store)

    return dumps({})
