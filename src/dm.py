from src.data_store import data_store
from src.error import InputError
from src.error import AccessError
from src.helpers import token_is_valid, decode_jwt

def dm_create_v1(token, u_ids):
    '''
    Create a dm
    Arguments:
        token - string
        u_ids - list of u_id

    Exceptions:
        AccessError - if token not valid
        InputError - if any u_id in u_ids are not actual user

    Return Value:
        Returns dm_id
    
    '''
    store = data_store.get()
    users = store['users']
    # if wrong token
    if not token_is_valid(token):
        raise AccessError('Invalid token')
    
    # convert token to auth_user_id
    user = decode_jwt(token)
    auid = user['auth_user_id']
    auth_user = next(user for user in users if user['auth_user_id'] == auid)
    u_ids.append(auid)

    # if u_id in u_ids does not refer to real users
    # check any user_id in u_ids is in users 
    list_of_all_u_id = []
    for user in users:
        list_of_all_u_id.append(user['auth_user_id'])
    for u_id in u_ids:
        if u_id not in list_of_all_u_id:
            raise InputError("Invalid u_id in u_ids")

    dm_id = len(store['dms']) + 1
    dm_name_list = []
    member_list = []
    #member_list.append(auth_user)
    for user in users:
        for u_id in u_ids:
            if user['auth_user_id'] ==  u_id:
                dm_name_list.append(user['handle_str'])
                member = {
                    'u_id' : user['auth_user_id'],
                    'email' : user['email'],
                    'name_first' : user['name_first'],
                    'name_last' : user['name_last'],
                    'handle_str' : user['handle_str']
                }
                member_list.append(member)
    sorted_dm_name_list = sorted(dm_name_list)
    dm_name = ', '.join(sorted_dm_name_list)
    store['dms'].append({
                'dm_id': dm_id, 
                'name' : dm_name, 
                'message': [],
                'owner' :  auth_user,
                'all_members' : member_list
                })

    #save it
    data_store.set(store)
    return dm_id



def dm_messages(token, dm_id, start):
    store = data_store.get()
    dms = store['dms']
    #users = store['users']

    if not token_is_valid(token):
        raise AccessError

    decoded_token = decode_jwt(token)
    auth_user_id = decoded_token['auth_user_id']

    dm = next((item for item in dms if item['dm_id'] == dm_id), None)
    
    '''
    user = next((item for item in users if item['auth_user_id'] == auth_user_id), None)
    if user is None:
        raise AccessError("Invalid auth_user_id")
    '''

    # if dm_id does not refer to a valid dm
    if dm is None:
        raise InputError("Invalid dm_id")

    if not any(item['u_id'] == auth_user_id for item in dm['all_members']):
        raise AccessError("No such user in dm")

    if start > len(dm['message']):
        raise InputError("Invalid start value")
	
    messages = dm['message']
    return_messages = []

    if start + 50 > len(messages):
        end = -1
        i = 0
        # if i is smaller than start, do nothing, else put the message into a new list
        for message in reversed(messages):
            if i < start:
                i = i + 1
            else:
                return_messages.append(message)
    else:
        end = start + 50
        i = 0
        # if i is smaller than start, do nothing, else put the message into a new list until end is reach
        for message in reversed(messages):
            if i < start:
                i = i + 1
            elif start < i <= end:
                return_messages.append(message)
                i = i + 1
            else:
                break
    return {
        'messages': return_messages, 'start': start, 'end': end,
        }

def dm_list_v1(token):
    '''
    This function will list the dms in which the authorised user is a member
    Argument: 
        token, type: string

    Exceptions: 
        AccessError: invalid or expired token

    Return value:
        Returns a dictionary containing a list of the dms that the relevant user id is in
        Each dm is a dictionary containing the dm_id and the name of the dm
    '''
    # Get the datastore
    store = data_store.get()

    # If the token does not belong to a registered user or is from an expired session
    if not token_is_valid(token):
        raise AccessError('No user id found')
    
    # Obtain the authorised user's auth_user_id
    decoded_token = decode_jwt(token)
    auth_user_id = decoded_token['auth_user_id']

    # Get the list of dms from the datastore
    dms = store['dms']
    # The list of dms to be returned
    return_dms = []

    # for every dm that the user is a member of, get the name and dm_id and
    # put it into the return_dms list
    for dm in dms:
        for member in dm['all_members']:
            if member['u_id'] == auth_user_id:
                new_dm = {}
                new_dm['dm_id'] = dm['dm_id']
                new_dm['name'] = dm['name']
                return_dms.append(new_dm)
                
    return {'dms' : return_dms}

def dm_leave_v1(token, dm_id):
    '''
    This function will allow the user to leave a dm
    Argument: 
        token, type: string
        dm_id, type: int

    Exceptions: 
        AccessError: invalid or expired token
        AccessError: The user attempting to leave is not a dm member
        InputError: If dm_id does not belong to a dm

    Return value:
        Returns an empty dictionary
    '''
    store = data_store.get()
    dms = store['dms']

    if not token_is_valid(token):
        raise AccessError

    decoded_token = decode_jwt(token)
    auid = decoded_token['auth_user_id']
    
    dm = next((item for item in dms if item['dm_id'] == dm_id), None)

    if dm is None:
        raise InputError
    
    user_to_leave = next((item for item in dm['all_members'] if item['u_id'] == auid), None)

    if user_to_leave is None:
        raise AccessError

    dm['all_members'].remove(user_to_leave)

    data_store.set(store)

    return {}
    
def dm_details_v1(token, dm_id):
    '''
    This function provides basic details (name and member details) about the channel that authorised member is a part of.

    Arguments:
        token, type: string
        channel_id, type: int

    Exceptions:
        InputError  - Occurs when dm_id does not refer to a valid dm
        AccessError - Occurs when the dm_id is valid and and the authorised user is not a member of the dm
        AccessError - Invalid or expired token

    Return Value:
        Returns a dictionary containing:
        name - name of dm
        members - all the members in the dm

    '''
    store = data_store.get()
    dms = store['dms']

    # If the token does not belong to a registered user or is from an expired session
    if not token_is_valid(token):
        raise AccessError
    
    # Grab the details of the authorised user and place them in variables
    decoded_token = decode_jwt(token)
    auth_user_id = decoded_token['auth_user_id']

    dm = next((item for item in dms if item['dm_id'] == dm_id), None)
    
    # if channel_id does not refer to a valid channel 
    if dm is None:
        raise InputError("Invalid dm_id")
    
    # if authorised user is not a member of the channel
    if not any(item['u_id'] == auth_user_id for item in dm['all_members']):
        raise AccessError("No such user in the dm")
    
    # put the detail we need from the channel to the return channel
    return_dm = {}
    return_dm['name'] = dm['name']
    return_dm['members'] = dm['all_members']

    return return_dm

def dm_remove_v1(auth_user_id, dm_id):
    '''
    This function will remove the dm the authorised user is in
    Argument: 
        auth_user_id, type: int
        dm_id, type: int

    Exceptions: 
        AccessError: Invalid or expired token
        AccessError: User is not a part of dm_id
        InputError: No dm_id found

    Return value:
        Returns an empty dictionary
    '''
    store = data_store.get()
    dm = store['dms']
    found_dm_obj = None
    found_dm_obj_idx = 0
    for idx, dm in enumerate(dm):
        if dm['dm_id'] is dm_id:
            found_dm_obj_idx = idx
            found_dm_obj = dm
            break

    if found_dm_obj is None:
        raise InputError('No dm found with the provided ID')

    # Checking if user is part of members within dm
    if auth_user_id is not found_dm_obj['owner']['auth_user_id']:
        raise AccessError('User is not part of the provided dm id')

    del store['dms'][found_dm_obj_idx]

    data_store.set(store)
    return {}