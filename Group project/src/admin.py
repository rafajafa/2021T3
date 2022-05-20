from src.data_store import data_store
from src.error import InputError
from src.error import AccessError
from src.helpers import token_is_valid, decode_jwt

def admin_user_remove_v1(token, u_id):
    '''
    This function will remove the user specified by u_id from Streams
    Argument: 
        token, type: string
        u_id, type: int

    Exceptions: 
        AccessError: invalid or expired token
        AccessError: the authorised user is not a global owner
        InputError: u_id does not refer to a valid user
        InputError: u_id refers to a user who is the only global owner

    Return value:
        Returns an empty dictionary
    '''
    # Get the datastore
    store = data_store.get()
    users = store['users']
    channels = store['channels']
    dms = store['dms']

    # If the token does not belong to a registered user or is from an expired session
    if not token_is_valid(token):
        raise AccessError('No user id found')
    
    # Obtain the authorised user's auth_user_id
    decoded_token = decode_jwt(token)
    auth_user_id = decoded_token['auth_user_id']

    # Find the user who is attempting to remove someone and ensure they are a global owner 
    user_remover = next((item for item in users if item['auth_user_id'] == auth_user_id), None)
    if not user_remover['is_global']:
        raise AccessError
    
    # Find the user who is to be removed, and raise an error if they don't exist
    user_to_be_removed = next((item for item in users if item['auth_user_id'] == u_id), None)
    if user_to_be_removed is None:
        raise InputError
    
    # Ensure the only global owner isn't trying to remove themselves
    if auth_user_id == u_id:
        raise InputError

    # Change the user's status to that of a removed user. The first key 'is_removed' will be used to distinguish
    # rmeoved and active users in other functions
    user_to_be_removed['is_removed'] = True
    user_to_be_removed['name_first'] = 'Removed'
    user_to_be_removed['name_last'] = 'user'

    # Edit their messages to show that they are removed
    for channel in channels:
        for message_dict in channel['messages']:
            if message_dict['u_id'] == u_id:
                message_dict['message'] = 'Removed user'

    for dm in dms:
        for message_dict in dm['message']:
            if message_dict['u_id'] == u_id:
                message_dict['message'] = 'Removed user'

    data_store.set(store)

    return {}

def admin_userpermission_change_v1(token, user_id, permission_id):
    '''
    promote or demote a user
    Arguments:
        token - string
        user_id - int
        permission_id - int - either 1 or 2

    Exceptions:
        AccessError - if token not valid
        InputError - if user_id dont dont match any user
        AccessError - if auth user is not a global user
        InputError - if permission_id is not 1 or 2
        InputError - try to demode the only global user

    Return Value:
        Returns nothing
    
    '''
    store = data_store.get()
    users = store['users']

    # if wrong token
    if not token_is_valid(token):
        raise AccessError("Invalid Token")

    user = next((item for item in users if item['auth_user_id'] == user_id), None)

    # if no such user in users 
    if user is None:
        raise InputError("Invalid auth_user_id")

    # convert token to auth_user_id
    auth_user = decode_jwt(token)
    auth_user_id = auth_user['auth_user_id']

    auth_user = next(item for item in users if item['auth_user_id'] == auth_user_id)

    if auth_user['is_global'] is False:
        raise AccessError('Auth user not a global user')
    
    if permission_id != 1 and permission_id != 2:
        raise InputError('Wrong permissio_id')
    
    count = 0

    for item in users:
        if item['is_global'] is True:
            count += 1

    if count <= 1 and user_id == auth_user_id and permission_id == 2:
        raise InputError('u_id is the only global user')
    
    if permission_id == 1:
        user['is_global'] = True
    else:
        user['is_global'] = False
    
    #save it
    data_store.set(store)
    return{}