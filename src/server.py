import re
import sys
import signal
import jwt
import json
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError, AccessError
from src import config
from src.auth import auth_register_v1, auth_login_v1, auth_logout_v1
from src.channels import channels_create_v1, channels_listall_v1, channels_list_v1
from src.channel import channel_addowner_v1, channel_removeowner_v1, channel_join_v1, channel_leave_v1, channel_messages_v1, channel_invite_v1, channel_details_v1
from src.message import message_send_v1, message_senddm_v1, message_remove_v1, message_edit_v1
from src.other import clear_v1, SECRET
from src.helpers import token_is_valid, decode_jwt, save
from src.user import users_all, user_profile_set_email, user_profile_set_name, user_profile_v1, user_set_handle_v1
from src.admin import admin_user_remove_v1, admin_userpermission_change_v1
from src.dm import dm_create_v1, dm_messages, dm_list_v1, dm_leave_v1, dm_details_v1, dm_remove_v1
from src.data_store import data_store
#from src.helpers import save, retrieve_data

def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)


#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS
store = data_store.get()
try:
    with open('database.json', 'r') as FILE:
        store = json.load(FILE)
    data_store.set(store)
except Exception:
    pass

# Example
@APP.route('/auth/register/v2', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = data['password']
    name_first = data['name_first']
    name_last = data['name_last']
    try:
        reg_ret = auth_register_v1(email, password, name_first, name_last)
        save()
        return dumps({
        'token': reg_ret['token'],
        'auth_user_id': reg_ret['auth_user_id']
        })
    except InputError:
        return InputError('InputError')

@APP.route('/auth/login/v2', methods = ['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    try:
        login_ret = auth_login_v1(email, password)
        save()
        return dumps({
            'token': login_ret['token'],
            'auth_user_id': login_ret['auth_user_id']
        })
    except InputError:
        return InputError('InputError')


@APP.route("/auth/logout/v1", methods = ['POST'])
def logout_v1():
    data = request.get_json()
    token = data['token']

    if not token_is_valid(token):
        return AccessError('Invalid token')
    
    # convert token to auth_user_id
    user = jwt.decode(token, SECRET, algorithms=['HS256'])
    auid = user['auth_user_id']
    session_id = user['session_id']
    try:
        auth_logout_v1(auid, session_id)
        save()
        return dumps({'success':True}), 200
    except AccessError:
        return AccessError('AccessError')
    except InputError:
        return InputError('InputError')


@APP.route('/channels/create/v2', methods = ['POST'])
def createchannel():
    data = request.get_json()
    token = data['token']
    name = data['name']
    is_public = data['is_public']

    if not token_is_valid(token):
        return AccessError('AccessError')

    decoded_token = decode_jwt(token)
    auth_user_id = decoded_token['auth_user_id']
    try: 
        channel_create_return = channels_create_v1(auth_user_id, name, is_public)
        save()
        return dumps(channel_create_return)

    except AccessError:
        return AccessError('AccessError')
    except InputError:
        return InputError('InputError')

@APP.route('/channels/list/v2', methods = ['GET'])
def channellist():
    token = request.args.get("token")

    if not token_is_valid(token):
        return AccessError('AccessError')

    decoded_token = decode_jwt(token)
    auth_user_id = decoded_token['auth_user_id']

    try: 
        channel_list_return = channels_list_v1(int(auth_user_id))
        save()
        return dumps(channel_list_return)

    except AccessError:
        return AccessError('AccessError')
    except InputError:
        return InputError('InputError')

@APP.route("/channels/listall/v2", methods = ['GET'])
def channels_listall_v2():
    token = request.args.get("token")

    print(token)
    if not token_is_valid(token):
        return AccessError('AccessError')
    # convert token to auth_user_id
    user = decode_jwt(token)
    auth_user_id = user['auth_user_id']

    try:   
        ret = channels_listall_v1(int(auth_user_id))
        save()
        return dumps(ret)
    except AccessError:
        return AccessError('AccessError')
    except InputError:
        return InputError('InputError')

#ask ayoob
@APP.route('/channel/addowner/v1', methods = ['POST'])
def channeladdowner():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']

    if not token_is_valid(token):
        return AccessError('AccessError')

    try: 
        add_owner_return = channel_addowner_v1(token, channel_id, u_id)
        save()
        return dumps(add_owner_return)
    except AccessError:
        return AccessError('AccessError')
    except InputError:
        return InputError('InputError')

@APP.route("/channel/messages/v2", methods = ['GET'])
def channel_messages_v2():
    token = request.args.get("token")
    channel_id = request.args.get("channel_id")
    start = request.args.get("start")

    if not token_is_valid(token):
        return AccessError('Invalid token')
    # convert token to auth_user_id
    user = jwt.decode(token, SECRET, algorithms=['HS256'])
    auth_user_id = user['auth_user_id']
    
    try:
        ret = channel_messages_v1(int(auth_user_id), int(channel_id), int(start))
        print(ret)
        save()
        return dumps(ret)
    except AccessError:
        return AccessError('AccessError')
    except InputError:
        return InputError('InputError')

@APP.route('/channel/invite/v2', methods = ['POST'])
def channel_invite():
    data = request.get_json()
    channel_id = data['channel_id']
    token = data['token']
    u_id = data['u_id']

    if not token_is_valid(token):
        return AccessError('Invalid token')

    decoded_token = decode_jwt(token)
    auth_user_id = decoded_token['auth_user_id']

    try:
        channel_invite_return = channel_invite_v1(auth_user_id, channel_id, u_id)
        save()
        return dumps(channel_invite_return)
    except AccessError:
        return AccessError('AccessError')
    except InputError:
        return InputError('InputError')

@APP.route('/channel/join/v2', methods=['POST'])
def join():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    
    if not token_is_valid(token):
        return AccessError('AccessError')

    decoded_token = decode_jwt(token)
    auid = decoded_token['auth_user_id']
    
    try:
        channel_join_v1(auid,channel_id)
        save()          
        return dumps({})
    
    except AccessError:
        return AccessError('AccessError')
    except InputError:
        return InputError('InputError')

@APP.route('/channel/leave/v1', methods=['POST'])
def channel_leave():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']

    try:
        channel_leave_return = channel_leave_v1(token,channel_id)
        save()         
        return dumps(channel_leave_return)
    
    except AccessError:
        return AccessError('AccessError')
    except InputError:
        return InputError('InputError')

@APP.route('/channel/details/v2', methods = ['GET'])
def channel_details():
    token = request.args.get("token")
    channel_id = request.args.get("channel_id")

    if not token_is_valid(token):
        return AccessError('AccessError')

    decoded_token = decode_jwt(token)
    auth_user_id = decoded_token['auth_user_id']
    
    try:
        channel_details_return = channel_details_v1(int(auth_user_id), int(channel_id))
        save()
        return dumps(channel_details_return)
    except AccessError:
        return AccessError('AccessError')
    except InputError:
        return InputError('InputError')

@APP.route('/channel/removeowner/v1', methods = ['POST'])
def remove_channel_owner():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']

    try:
        channel_removeowner_v1(token, channel_id, u_id)
        save()
        return dumps({})
    except AccessError:
        return AccessError('AccessError')
    except InputError:
        return InputError('InputError')

@APP.route('/message/send/v1', methods = ['POST'])
def message_send():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    message = data['message']
    try:
        message_ret = message_send_v1(token, channel_id, message)
        save()
        return dumps({'message_id': message_ret['message_id']})
    except AccessError:
        return AccessError('AccessError')
    except InputError:
        return InputError('InputError')

@APP.route('/message/remove/v1', methods=['DELETE'])
def messages_remove():
    '''
    This function will remove a message from the channel or dm to which it was sent
    Argument: 
        token, type: string
        message_id, type: int
    
    Exceptions: 
        AccessError: invalid or expired token
        AccessError: the authorised user is neither the sender of the message nor an owner of the channel/dm
        InputError: message_id does not belong to a message in any of the dms or channels
    
    Return value:
        Returns a dictionary containing the message_id of the new message
    '''
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']

    try:
        message_remove_return = message_remove_v1(token, message_id)
        save()
        return dumps(message_remove_return)
    except AccessError:
        return AccessError('AccessError')
    except InputError:
        return InputError('InputError')


@APP.route("/message/senddm/v1", methods = ['POST'])
def senddm():
    data = request.get_json()
    token = data['token']
    dm_id = data['dm_id']
    message = data['message']

    try:
        message_senddm_return = message_senddm_v1(token, dm_id, message)
        save()
        return dumps(message_senddm_return)
    except AccessError:
        return AccessError('AccessError')
    except InputError:
        return InputError('InputError')

@APP.route('/message/edit/v1', methods = ['PUT'])
def edit_message():
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    message = data['message']
    decoded_token = decode_jwt(token)
    auth_user_id = decoded_token['auth_user_id']
    try:
        message_edit_return = message_edit_v1(auth_user_id, message_id, message)
        save()
        return dumps(message_edit_return)
    except AccessError:
        return AccessError('AccessError')
    except InputError:
        return InputError('InputError')

@APP.route('/users/all/v1', methods = ['GET'])
def usersall():
    token = request.args.get("token")
    
    if not token_is_valid(token):
        return AccessError('AccessError')

    try: 
        users_all_return = users_all(token)
        save()
        return dumps(users_all_return)
    
    except AccessError:
        return AccessError('AccessError')
    except InputError:
        return InputError('InputError')
    
@APP.route('/dm/messages/v1', methods = ['GET'])
def dmmessages():
    token = request.args.get("token")
    dm_id = request.args.get("dm_id")
    start = request.args.get("start")

    try: 
        dm_messages_return = dm_messages(token, int(dm_id), int(start))
        save()
        return dumps(dm_messages_return)

    except AccessError:
        return AccessError('AccessError')
    except InputError:
        return InputError('InputError')

@APP.route("/dm/list/v1", methods=['GET'])
def dm_list():
    token = request.args.get('token')
    try:
        dm_list_ret = dm_list_v1(token)
        save()
        return dumps({'dms': dm_list_ret['dms']})
    except AccessError:
        return AccessError('AccessError')
    except InputError:
        return InputError('InputError')

@APP.route("/dm/create/v1", methods = ['POST'])
def dm_create():
    data = request.get_json()
    token = data['token']
    u_ids = data['u_ids']
    
    try:
        dm_id = dm_create_v1(token, u_ids)
        save()
        return dumps({"dm_id" : dm_id})
    except AccessError:
        return AccessError('AccessError')
    except InputError:
        return InputError('InputError')

@APP.route('/dm/leave/v1', methods=['POST'])
def dm_leave():
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
    data = request.get_json()
    token = data['token']
    dm_id = data['dm_id']
    
    if not token_is_valid(token):
        return AccessError('AccessError')
    try: 
        dm_leave_return = dm_leave_v1(token, dm_id)
        save()
        return dumps(dm_leave_return)
    except AccessError:
        return AccessError('AccessError')
    except InputError:
        return InputError('InputError')

@APP.route("/dm/details/v1", methods = ['GET'])
def dm_details():

    token = request.args.get("token")
    dm_id = request.args.get("dm_id")

    try:
        details = dm_details_v1(token, int(dm_id))
        save()
        return dumps(details)
    except AccessError:
        return AccessError('AccessError')
    except InputError:
        return InputError('InputError')

@APP.route("/user/profile/v1", methods = ['GET'])
def profile_v1():
    #data = request.get_json()
    #token = data['token']
    #auth_user_id = data['u_id']

    token = request.args.get("token")
    user_id = request.args.get("u_id")

    try:
        profile_dict = user_profile_v1(token, int(user_id))
        save()
        return dumps({'user': profile_dict})
    except AccessError:
        return AccessError('AccessError')
    except InputError:
        return InputError('InputError')

@APP.route('/user/profile/setname/v1', methods=['PUT'])
def setname():
    data = request.get_json()
    token = data['token']
    name_first = data['name_first']
    name_last = data['name_last']

    try: 
        set_name_return = user_profile_set_name(token, name_first, name_last)
        save()
        return dumps(set_name_return)

    except AccessError:
        return AccessError('AccessError')
    except InputError:
        return InputError('InputError')

@APP.route('/user/profile/setemail/v1', methods = ['PUT'])
def setemail():
    data = request.get_json()
    token = data['token']
    email = data['email'] 

    if not token_is_valid(token):
        return AccessError('AccessError')
    
    try: 
        set_email_return = user_profile_set_email(token, email)
        save()
        return dumps(set_email_return)

    except AccessError:
        return AccessError('AccessError')

    except InputError:
        return InputError('InputError')

@APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def sethandle():
    data = request.get_json()
    token = data['token']
    handle_str = data['handle_str']
    try:
        user_set_handle_v1(token, handle_str)
        save()
        return dumps({})
    except InputError:
        return InputError('InputError')
    except AccessError:
        return AccessError('AccessError')

@APP.route('/admin/user/remove/v1', methods = ['DELETE'])
def admin_user_remove():
    data = request.get_json()
    token = data['token']
    u_id = data['u_id']
    try:
        admin_user_remove_v1(token, u_id)
        save()
        return dumps({})
    except InputError:
        return InputError('InputError')
    except AccessError:
        return AccessError('AccessError')

@APP.route("/admin/userpermission/change/v1", methods = ['POST'])
def admin_userpermission_change():
    data = request.get_json()
    token = data['token']
    user_id = data['u_id']
    permission_id = data['permission_id']
    
    try:
        admin_userpermission_change_v1(token, user_id, permission_id)
        save()
        return dumps({'success':True}), 200
    except AccessError:
        return AccessError('AccessError')
    except InputError:
        return InputError('InputError')

@APP.route('/clear/v1', methods = ['DELETE'])
def clear():
    clear_v1()
    save()
    return dumps({}), 200


# Completed Route 
@APP.route('/dm/remove/v1', methods = ['DELETE'])
def dm_remove():
    data = request.get_json()
    token = data['token']
    decoded_token = decode_jwt(token)
    auth_user_id = decoded_token['auth_user_id']
    dm_id = data['dm_id']
    try:
        dm_remove_return = dm_remove_v1(auth_user_id, dm_id)
        save()
        return dumps(dm_remove_return)
    except AccessError:
        return AccessError('AccessError')
    except InputError:
        return InputError('InputError')

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
