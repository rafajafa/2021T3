from src.data_store import data_store
from src.error import InputError
from src.error import AccessError
from src.helpers import decode_jwt, token_is_valid, generate_id, generate_message_id
from datetime import datetime
from datetime import timezone

def message_send_v1(token, channel_id, message):
    '''
    This function will send a message to the specified channel
    Argument: 
        token, type: string
        channel_id, type: int
        message, type: string

    Exceptions: 
        AccessError: invalid or expired token
        AccessError: channel_id is valid and the authorised user is not a member of the channel
        InputError: channel_id does not refer to a valid channel
        InputError: length of message is less than 1 or over 1000 characters

    Return value:
        Returns a dictionary containing the message_id of the new message
    '''
    store = data_store.get()
    channels = store['channels']
    
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

    # Get the members list of the channel
    members = channel['all_members']
    # Check if the authorised user is a channel member - if they aren't, raise an AccessError
    if not any(member['u_id'] == auth_user_id for member in members):
        raise AccessError
    
    # If the message is not in the correct length range
    if len(message) not in range(1,1001):
        raise InputError
    
    # Generate a message_id
    msg_id = generate_message_id()
    # Obtain the unix timestamp for the current time
    current_date_time = datetime.now()
    time_created = current_date_time.replace(tzinfo=timezone.utc).timestamp()

    # Create a dictionary with the required details of the message
    message_dict = {'message_id': msg_id, 'u_id': auth_user_id, 'message': message, 'time_created': time_created}

    # Add the new message to the messages list in the channel
    channel['messages'].append(message_dict)

    # Save the datastore
    data_store.set(store)

    # Return the message_id
    return {'message_id': msg_id}

def message_senddm_v1(token, dm_id, message):
    '''
    Send a message to dm
    Arguments:
        token - string
        dm_id - int
        message - string

    Exceptions:
        AccessError - if token not valid
        InputError - if dm_id is invalid
        AccessError - if the user is not a member of dm
        InputError - if the message is less than 1 char or bigger than 1000 char

    Return Value:
        Returns message_id

    '''

    store = data_store.get()
    users = store['users']
    dms = store['dms']

    # if wrong token
    if not token_is_valid(token):
        raise AccessError("Invalid Token")

    # convert token to auth_user_id
    #user = jwt.decode(token, SECRET, algorithms=['HS256'])
    user = decode_jwt(token)
    auth_user_id = user['auth_user_id']
    user = next((item for item in users if item['auth_user_id'] == auth_user_id), None)

    dm = next ((item for item in dms if item['dm_id'] == dm_id), None)
    # if no such dm in dms
    if dm is None:
        raise InputError('Invalid dm_id')

    user_handle = user['handle_str']
    # if user and dm_id is valid but he is not in the dm 
    if not user_handle in dm['name']:
        raise AccessError('User not a member of dm')

    # if message too long or too short
    if len(message) not in range(1,1001):
        raise InputError('Invalid message length')

    # create message_id
    message_id = generate_message_id()
    # Obtain the unix timestamp for the current time
    current_date_time = datetime.now()
    time_created = current_date_time.replace(tzinfo=timezone.utc).timestamp()

    # Create a dictionary with the required details of the message
    message_dict = {'message_id': message_id, 'u_id': auth_user_id, 'message' : message, 'time_created': time_created}
    dm['message'].append(message_dict)

    return {"message_id" : message_id}

def message_remove_v1(token, message_id):
    '''
    Removes a message from dm or channel
    Arguments:
        token - string
        message_id - int

    Exceptions:
        AccessError - if token not valid
        InputError - if message_id is invalid
        AccessError - if the user is not an owner or the person who
                        sent the message 

    Return Value:
        Returns an empty list

    '''
    store = data_store.get()
    channels = store['channels']
    dms = store['dms']

    # if wrong token
    if not token_is_valid(token):
        raise AccessError

    decoded_token = decode_jwt(token)
    auid = decoded_token['auth_user_id']
    
    msg_not_found = True

    for channel in channels:
        messages = channel['messages']
        for message in messages:
            if message['message_id'] == message_id:
                msg_not_found = False
                owners = channel['owner_members']
                if message['u_id'] != auid and not any(owner['u_id'] == auid for owner in owners):
                    raise AccessError
                messages.remove(message)
    
    for dm in dms:
        messages = dm['message']
        for message in messages:
                if message['message_id'] == message_id:
                    msg_not_found = False
                    owner = dm['owner']
                    if message['u_id'] != auid and owner['auth_user_id'] != auid:
                        raise AccessError
                    messages.remove(message)
                
    
    if msg_not_found:
        raise InputError

    data_store.set(store)
    return {}

def message_edit_v1(auth_user_id, message_id, message):
    '''
    Given a message, update its text with new text. If the new message is an empty string, the message is deleted.

    Arguments:
        token (string)    - unique id for an authorised user that expires.
        message_id (integer)    - unique id of the dm.
        message (string)      - messages that are being edited.

    Exceptions:
        InputError  - Occurs when length of message is over 1000 characters, 
                      message_id does not refer to a valid message within a channel/DM that the authorised user has joined.
        AccessError - Occurs when message_id refers to a valid message in a joined channel/DM and none of the following are true:
                      the message was sent by the authorised user making this request,
                      the authorised user has owner permissions in the channel/DM.

    Return Value:
        Returns an empty object.
    '''
    if message is None or len(message) > 1000:
        raise InputError('Message not valid.')
    
    store = data_store.get()
    channels = store['channels']
    dms = store['dms']

    # Check if message id is valid by looping through user_channels a user belongs to
    # and looping through messages of the channel to see if the message_id matches the provided message_id

    found_message_obj = None
    found_message_obj_idx = 0
    found_channel_obj = None
    found_channel_obj_idx = 0
    found_dm_obj = None
    found_dm_obj_idx = 0

    # Find the message and channel linked to the message id provided
    for channel_idx, channel in enumerate(channels):
        messages = channel['messages']
        for message_idx, message_obj in enumerate(messages):
            if message_obj['message_id'] is message_id:
                found_message_obj = message_obj
                found_message_obj_idx = message_idx
        if found_message_obj is not None:
            found_channel_obj = channel
            found_channel_obj_idx = channel_idx

    # Find the message and dm linked to the message id provided
    if found_channel_obj is None:
        for dm_idx, dm in enumerate(dms):
            messages = dm['message']
            for message_idx, message_obj in enumerate(messages):
                if message_obj['message_id'] is message_id:
                    found_message_obj = message_obj
                    found_message_obj_idx = message_idx
            if found_message_obj is not None:
                found_dm_obj = dm
                found_dm_obj_idx = dm_idx

    if found_message_obj is None:
        raise InputError(dms)
    
    # Check if the user is authorised to edit the message
    is_auth_user_channel_owner = False

    if found_channel_obj is not None:
        for channel_owner in found_channel_obj['owner_members']:
            if channel_owner['u_id'] is auth_user_id:
                is_auth_user_channel_owner = True
                break
    else:
        if found_dm_obj['owner']['auth_user_id'] is auth_user_id:
            is_auth_user_channel_owner = True

    if found_message_obj['u_id'] is not auth_user_id and is_auth_user_channel_owner is False:
        raise AccessError('Auth user is neither a message owner nor a channel owner')

    # Delete if message is blank or Edit message and assign to found dm/channel
    if (message is None or message is ''):
        if found_channel_obj is not None:
            del found_channel_obj['messages'][found_message_obj_idx]
        else:
            del found_dm_obj['message'][found_message_obj_idx]
    else:
        if found_channel_obj is not None:
            found_channel_obj['messages'][found_message_obj_idx]['message'] = message
        else:
            found_dm_obj['message'][found_message_obj_idx]['message'] = message

    # Replace the channel/dm obj in the store with the modified one
    if found_channel_obj is not None:
        store[found_channel_obj_idx] = found_channel_obj
    else:
        store[found_dm_obj_idx] = found_dm_obj
    
    data_store.set(store)
    return {}