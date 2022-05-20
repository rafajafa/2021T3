from flask import Flask, request
from json import dumps
from number_fun import multiply_by_two, print_message, sum_list_of_numbers, sum_iterable_of_numbers, is_in, index_of_number

APP = Flask(__name__)
PORT = 5000

@APP.route('/multiply_by_two', methods = ['GET'])
def multiply_by_two_v1():
    num = int(request.args.get("num"))
    ret = multiply_by_two(num)
    return dumps({'ret': ret})

@APP.route('/print_message', methods = ['GET'])
def print_message_v1():
    string = request.args.get("string")
    print_message(string)
    return dumps({'success':True}), 200

@APP.route('/sum_list_of_numbers', methods = ['GET'])
def sum_list_of_numbers_v1():
    parameter = request.args.get("list")
    parameters = parameter.split(',')
    list = []
    for parameter in parameters:
        list.append(int(parameter))

    ret = sum_list_of_numbers(list)
    return dumps({'ret': ret})

@APP.route('/sum_iterable_of_numbers', methods = ['GET'])
def sum_iterable_of_numbers():
    parameter = request.args.get("list")
    parameters = parameter.split(',')
    list = []
    for parameter in parameters:
        list.append(int(parameter))

    ret = sum_iterable_of_numbers(list)
    return dumps({'ret': ret})

@APP.route('/is_in', methods = ['GET'])
def is_in_v1():
    needle = request.args.get("needle")
    haystack = request.args.get("haystack")
    ret = is_in(needle, haystack)
    return dumps({'ret': ret})

@APP.route('/index_of_number', methods = ['GET'])
def index_of_number_v1():
    item = int(request.args.get("item"))
    list = request.args.get("list")
    ret = index_of_number(item, list)
    return dumps({'ret': ret})

if __name__ == "__main__":
    APP.run(port=PORT, debug=True)
