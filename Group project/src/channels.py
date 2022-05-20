from src.data_store import data_store
from src.error import InputError

def channels_list_v1(auth_user_id):
    '''
    This function will list the channels containing the relevant user id
    Argument: 
        auth_user_id, type: int

    Exceptions: 
        AccessError: no such auth_user_id found in the database

    Return value:
        return a dictionary of a list of dictionary containing the 
        channels the relevant user id is in
    '''
    store = data_store.get()

    '''
    users = store['users']
    # check if the user is in users, else access error
    if any(d['auth_user_id'] == auth_user_id for d in users):
        for user in users:
            if user['auth_user_id'] == auth_user_id:
                break
    else:
        raise AccessError('No user id found')
    '''
    channels = store['channels']
    return_channels = []
    # for every channel that the user is a member of, get the name and channel id and
    # put it into a list of dictionary 
    for channel in channels:
        for members in channel['all_members']:
            if members['u_id'] == auth_user_id:
                new_channel = {}
                new_channel['channel_id'] = channel['channel_id']
                new_channel['name'] = channel['name']
                return_channels.append(new_channel)
                
    return {'channels' : return_channels}


def channels_listall_v1(auth_user_id):
    '''
    This function will list all the channel whether it is public or not
    Argument: 
        auth_user_id, type: int

    Exceptions: 
        AccessError: no such auth_user_id found in the database

    Return value:
        return a dictionary of a list of dictionary containing all the channel

    '''
    store = data_store.get()
    channels = store['channels']
    return_channels = []
    
    # if user is a member, copy all the channels and their name into
    # a new list of dictionary and return the new list
    # dont need to check if user_id is valid because it was check before
    '''
    users = store['users']
    if any(d['auth_user_id'] == auth_user_id for d in users):
        for channel in channels:
            new_channel = {}
            new_channel["channel_id"] = channel["channel_id"]
            new_channel["name"] = channel["name"]
            return_channels.append(new_channel)
    else:
        raise AccessError("No user id found")
    '''
    for channel in channels:
        new_channel = {}
        new_channel["channel_id"] = channel["channel_id"]
        new_channel["name"] = channel["name"]
        return_channels.append(new_channel)

    return {
        'channels': return_channels
        }


def channels_create_v1(auth_user_id, name, is_public):
    '''
    This function will create a new channel and add a new channel to the system
        auth_user_id, type: int
        name, type: string
        is_public, type: boolean

    Exceptions: 
        AccessError: no such auth_user_id found in the database
        InputError: length of channel name is too short

    Return value:
        return a dictionary of channel_id of the new channel,
        the channel_id for the new channel will be the number 
        of total channels in the system + 1
    '''
    store = data_store.get()
    users = store['users']
    
    #find the user with the auth_user_id parameter
    target_user = next(item for item in users if item['auth_user_id'] == auth_user_id)

    #if channel_name is not valid
    if len(name) > 20 or len(name) < 1:
        raise InputError('Length of name is less than 1 or more than 20 characters')
    
    target_user_specifics = {'u_id' : auth_user_id}
    # place info from target_user to the a new list without info for password, is_global and auth_user_id
    target_user_specifics.update({k:v for (k,v) in target_user.items() if (k != 'password' and k != 'is_global' and k != 'auth_user_id' and k != 'sessions' and k != 'is_removed')})

    channel_id = len(store['channels']) + 1

    store['channels'].append(
        {
        'channel_id': channel_id,
        'name': name,
        'owner_members': [target_user_specifics],
        'all_members': [target_user_specifics],
        'messages' : [],
        'is_public' : is_public,
        })
    
    data_store.set(store)
    
    return {
        'channel_id' : channel_id
    }


