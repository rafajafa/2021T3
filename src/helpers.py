import jwt
import json
from src.data_store import data_store

SECRET = 'C0Jp43mts6noiF4eXTawzthtRL1kRV'
ID_COUNT = 0

def token_is_valid(token):
    '''
    This function will return 
    Argument: 
        token, type: string

    Exceptions: 
        AccessError: No user registered with the encoded auth_user_id
        AccessError: No user with the encoded session_id

    Return value:
        returns a boolean - 'True' if the token belongs to a user that is logged in, 'False' otherwise

    '''
    store = data_store.get()
    users = store['users']
    try:
        decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError, jwt.DecodeError):
        return False

    auid = decoded_token['auth_user_id']
    session_id = decoded_token['session_id']

    user = next((item for item in users if item['auth_user_id'] == auid), None)
    if user == None:
        return False
    sessions = user['sessions']
    if session_id not in sessions:
        return False
    return True

def generate_jwt(auth_user_id, session_id):
    '''
    This function will return 
    Argument: 
        auth_user_id, type: int
        session_id, type: int

    Exceptions: 
        None

    Return value:
        returns a jwt with the given data
    '''
    return jwt.encode({'auth_user_id': auth_user_id, 'session_id': session_id}, SECRET, algorithm='HS256')

def decode_jwt(token):
    '''
    This function will return 
    Argument: 
        token, type: string

    Exceptions: 
        None

    Return value:
        returns the data encoded in a jwt
    '''
    return jwt.decode(token, SECRET, algorithms=['HS256'])

def generate_id():
    '''
    This function will return 
    Argument: 
        None

    Exceptions: 
        None

    Return value:
        returns a distinct integer whenever called
    '''
    store = data_store.get()
    store['ID_COUNT'] += 1
    data_store.set(store)
    return store['ID_COUNT']

def generate_message_id():
    '''
    This function will return 
    Argument: 
        None

    Exceptions: 
        None

    Return value:
        returns a distinct integer whenever called
    '''
    store = data_store.get()
    store['MSGID_COUNT'] += 1
    data_store.set(store)
    return store['MSGID_COUNT']

def save():
    store = data_store.get()
    with open('database.json', 'w') as FILE:
        json.dump(store, FILE)