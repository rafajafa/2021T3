from flask import Flask, request
from json import dumps

APP = Flask(__name__)
PORT = 5000

names = []

@APP.route("/names/add", methods = ["POST"])
def add_name():
    data = request.get_json()
    name1 = data['name']
    names.append(name1)
    return{}


@APP.route("/names", methods = ["GET"])
def get_names():
    return dumps({'name' : names})

@APP.route("/names/remove", methods = ["DELETE"])
def delete_name():
    data = request.get_json()
    name1 = data['name']
    names.remove(name1)
    return{}

@APP.route("/names/clear", methods = ["DELETE"])
def clear_names():
    names.clear()
    return{}

if __name__ == "__main__":
    APP.run(port=PORT, debug=True)


