from src.data_store import data_store
from src.error import InputError
from src.error import AccessError
from src.helpers import decode_jwt, token_is_valid

def channel_invite_v1(auth_user_id, channel_id, u_id):
    '''
    channel invite function lets all members of a channel invite a user.

    Arguments:
        auth_user_id, int    - member that is inviting
        channel_id, int    - id of the channel that invited member is joining
        u_id, int   - member that is being invited

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel, u_id does not refer to a valid user, u_id refers to a user who is already a member of the channel.
        AccessError - Occurs when auth_user_id does not refer to a valid user, auth_user_id is not a member of the channel.

    Return Value:
        Returns empty

    '''
    store = data_store.get()
    fetched_channel = None
    fetched_channel_idx = 0
    
    # Checking if channel exists
    for idx, channel in enumerate(store['channels']):
        if channel['channel_id'] == channel_id:
            fetched_channel = channel
            fetched_channel_idx = idx
            break
    
    '''
    # Checking if user inviting the other (auth_user_id) exists
    if not any(user['auth_user_id'] == auth_user_id for user in store['users']):
        raise AccessError('User not found')
    '''

    # Checking if user being invited (u_id) exists
    if not any(user['auth_user_id'] == u_id for user in store['users']):
        raise InputError('User not found')

    # Check if the channel exists
    if fetched_channel is None:
        raise InputError('Channel not found')

    # Check if the auth user is a member of channel
    if not any(member['u_id'] == auth_user_id for member in fetched_channel['all_members']):
        raise AccessError('Auth user not a member of channel')

    # Checking if invited user is already a member
    if any(member['u_id'] == u_id for member in fetched_channel['all_members']):
        raise InputError('User is already a member')


    # Grabbing uid info
    for user in store['users']:
        if user['auth_user_id'] == u_id:
            fetched_user = {'u_id' : u_id}
            fetched_user.update({k:v for (k,v) in user.items() if (k != 'password' and k != 'is_global' and k != 'auth_user_id' and k != 'sessions' and k != 'is_removed')})

    

    # Add user to fetched Channel members list.
    fetched_channel['all_members'].append(fetched_user)
    store['channels'][fetched_channel_idx] = fetched_channel
    data_store.set(store)

    return {}

def channel_details_v1(auth_user_id, channel_id):
    '''
    channel details function provides basic details about the channel that authorised member is a part of.

    Arguments:
        auth_user_id, int    - member that is inviting
        channel_id, int    - id of the channel that invited member is joining

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel
        AccessError - Occurs when auth_user_id does not refer to a valid user

    Return Value:
        Returns name - name of channel
        Returns is_public - whether channel is public or private
        Returns owner_members - all the owners of the channel
        Returns all_members - all the members of the channel

    '''
    store = data_store.get()
    #users = store['users']
    channels = store['channels']

    channel = next((item for item in channels if item['channel_id'] == channel_id), None)
    # Check if the auth_user_id is valid (i.e. if it belongs to a registered user)
    # user = next((item for item in users if item['auth_user_id'] == auth_user_id), None)
    
    '''
    # if no such user in users 
    if user is None:
        raise AccessError("Invalid auth_user_id")
    '''
    
    # if channel_id does not refer to a valid channel 
    if channel is None:
        raise InputError("Invalid channel")
    
    # if authorised user is not a member of the channel
    if not any(item['u_id'] == auth_user_id for item in channel['all_members']):
        raise AccessError("No such user in the channel")
    
    # put the detail we need from the channel to the return channel
    return_channel = {}
    return_channel['name'] = channel['name']
    return_channel['is_public'] = channel['is_public']
    return_channel['owner_members'] = channel['owner_members']
    return_channel['all_members'] = channel['all_members']

    return return_channel 

def channel_messages_v1(auth_user_id, channel_id, start):
    '''
    This function will return up to 50 msgs from the most recent msg

    Argument:
        auth_user_id: int
        channel_id: int
        start: int

    Exceptions:
        AccessError: auth_user_id is not in the list of users
        InputError: channel_id is not in the list of channels
        AccessError: user is not a member in the channel

    Return Value:
        return list of messages, start 
        return end as start + 50 if there are more the 50 msg after the start
        return end as -1 else
    '''
    store = data_store.get()
    channels = store['channels']
    #users = store['users']
    channel = next((item for item in channels if item['channel_id'] == channel_id), None)
    #user = next((item for item in users if item['auth_user_id'] == auth_user_id), None)
    # if no such user in users 
    '''
    if user is None:
        raise AccessError("Invalid auth_user_id")
    '''
    # if channel_id does not refer to a valid channel 
    if channel is None:
        raise InputError("Invalid channel")
    
    # if authorised user is not a member of the channel
    if not any(item['u_id'] == auth_user_id for item in channel['all_members']):
            raise AccessError("No such user in the channel member")
    
    # if start is greater than the total number of messages in the channel
    if start > len(channel['messages']):
        raise InputError("Invalid start value")

    messages = channel['messages']
    return_messages = []
    # if channel has less than 50 msg after start 
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

def channel_join_v1(auth_user_id, channel_id):
    '''
    Arguments:
        <auth_user_id> (int)    -  invited member
        <channel_id> (int)    -  joined channel

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel or the authorised user is already a member of the channel
        AccessError - Occurs when channel_id refers to a channel that is private and the authorised user is not already a channel member and is not a global owner

    Return Value:
        Returns empty
    '''
    store = data_store.get()
    users = store['users']
    
    #find the exist user
    for user in users:
        if auth_user_id == user['auth_user_id']:
            correct_user = user
	
	#find the correct channel
    channels = store['channels']
    valid_channel = False
    for channel in channels:
        if channel_id == channel['channel_id']:
            valid_channel = True
            correct_channel = channel
            break
    if not valid_channel:
        raise InputError
    
    #if the user is already in the channel
    all_members = correct_channel['all_members']
    for member in all_members:
        if correct_user['auth_user_id'] == member['u_id']:
            raise InputError
    
    #check whether the channel is private and user is global
    is_public = correct_channel['is_public']
    is_global = correct_user['is_global']
    if not is_public:
        if not is_global:
            raise AccessError
    
    #add the user to the channel
    correct_channel['all_members'].append({'u_id':correct_user['auth_user_id'],
	                                       'email':correct_user['email'],
	                                       'name_first':correct_user['name_first'],
	                                       'name_last':correct_user['name_last'],
	                                       'handle_str':correct_user['handle_str']})
    data_store.set(store)
    return {}

def channel_addowner_v1(token, channel_id, u_id):
    '''
    This function will add an owner of the specified channel
    Argument: 
        token, type: string
        channel_id, type: int
        u_id, type: int

    Exceptions: 
        AccessError: invalid or expired token
        AccessError: if the channel_id is valid and the authorised user is not a channel owner
        InputError: channel_id does not refer to a valid channel
        InputError: u_id does not refer to a valid user
        InputError: u_id refers to a user who is not a member of the channel
        InputError: u_id refers to a user who is currently the only owner of the channel

    Return value:
        Returns an empty dictionary
    '''
    store = data_store.get()
    channels = store['channels']
    users = store['users']

    decoded_token = decode_jwt(token)
    auth_user_id = decoded_token['auth_user_id']

    # Obtain the dictionary with the details of the specified channel from the datastore
    channel = next((item for item in channels if item['channel_id'] == channel_id), None)
    # Checks Valid Channel
    if channel is None:
        raise InputError("Invalid Channel")

    # Obtain the dictionary with the details of the specified member from the datastore
    owner_members = channel['owner_members']
    user_owner = next((item for item in owner_members if item['u_id'] == auth_user_id), None)
    # Checks valid owner
    if user_owner is None:
        raise AccessError("User have no permissions")

    # Obtain the dictionary with the details of the specified user from the datastore
    user = next((item for item in users if item['auth_user_id'] == u_id), None)
    # Check whether valid user
    if user is None:
        raise InputError("Invalid u_id")

    # Checks if the uid is a  member
    all_members = channel['all_members']
    member = next((item for item in all_members if item['u_id'] == u_id), None)
    if member is None:
        raise InputError("User Id is not a member")
    
    #Checks if the member is already an owner
    owner_members = channel['owner_members']
    own_member = next((item for item in owner_members if item['u_id'] == u_id), None)
    if own_member is not None:
        raise InputError("Member is already owner")

    for user in store['users']:
        if user['auth_user_id'] == u_id:
            fetched_user = {'u_id' : u_id}
            fetched_user.update({k:v for (k,v) in user.items() if (k != 'password' and k != 'is_global' and k != 'auth_user_id' and k != 'sessions' and k != 'is_removed')})

    channel['owner_members'].append(fetched_user)
    data_store.set(store)
    return {}

def channel_removeowner_v1(token, channel_id, u_id):
    '''
    This function will remove an owner of the specified channel
    Argument: 
        token, type: string
        channel_id, type: int
        u_id, type: int

    Exceptions: 
        AccessError: invalid or expired token
        AccessError: if the channel_id is valid and the authorised user is not a channel owner
        InputError: channel_id does not refer to a valid channel
        InputError: u_id does not refer to a valid user
        InputError: u_id refers to a user who is not an owner of the channel
        InputError: u_id refers to a user who is currently the only owner of the channel

    Return value:
        Returns an empty dictionary
    '''
    store = data_store.get()
    channels = store['channels']
    users = store['users']
    
    # If the token does not belong to a registered user or is from an expired session
    if not token_is_valid(token):
        raise AccessError
    
    # Grab the details of the authorised user and place them in variables
    decoded_token = decode_jwt(token)
    auth_user_id = decoded_token['auth_user_id']
    
    # Obtain the dictionary with the details of the specified channel from the datastore
    channel = next((item for item in channels if item['channel_id'] == channel_id), None)
    # if channel_id does not refer to a valid channel 
    if channel is None:
        raise InputError("Invalid channel")

    # Get the owners list of the channel
    owners = channel['owner_members']
    # Check if the authorised user is a channel owner - if they aren't, raise an AccessError
    if not any(owner['u_id'] == auth_user_id for owner in owners):
        raise AccessError
    
    # If there is no registered user with an auth_user_id of u_id
    if not any(user['auth_user_id'] == u_id for user in users):
        raise InputError
    
    # Obtain the dictionary with the details of the authorised user from the channel owners list
    user_to_be_removed = next((item for item in owners if item['u_id'] == u_id), None)
    # If there is no channel owner with an auth_user_id of u_id
    if user_to_be_removed is None:
        raise InputError
    
    # If the only remaining channel owner attempts to remove themselves
    if auth_user_id == u_id:
        raise InputError
    
    # Remove the user from the owners list
    channel['owner_members'].remove(user_to_be_removed)

    # Save the datastore
    data_store.set(store)

    return {}

def channel_leave_v1(token, channel_id):
    '''
    This function will allow users to leave channels they are in
    Argument: 
        token, type: string
        channel_id, type: int

    Exceptions: 
        AccessError: invalid or expired token
        AccessError: if the channel_id is valid and the authorised user is not a channel member
        InputError: if the channel_id does not belong to any channel

    Return value:
        Returns an empty dictionary
    '''
    store = data_store.get()
    channels = store['channels']

    if not token_is_valid(token):
        raise AccessError
    decoded_token = decode_jwt(token)
    auid = decoded_token['auth_user_id']
    
    # Obtain the dictionary with the details of the specified channel from the datastore
    channel = next((item for item in channels if item['channel_id'] == channel_id), None)
    # if channel_id does not refer to a valid channel 
    if channel is None:
        raise InputError("Invalid channel")

    
    user_to_be_removed = next((item for item in channel['all_members'] if item['u_id'] == auid), None)
    if user_to_be_removed is None:
        raise AccessError
    
    channel['all_members'].remove(user_to_be_removed)

    user_to_be_removed = next((item for item in channel['owner_members'] if item['u_id'] == auid), None)
    if user_to_be_removed is not None:
        channel['owner_members'].remove(user_to_be_removed)

    data_store.set(store)
    
    return {}