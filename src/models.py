import flask_login
from flask import Flask, request, json
from src.Connector import Connector
import os

app = Flask(__name__)

app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'database.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.secret_key = 'very ultra secret key'


login_manager = flask_login.LoginManager()
login_manager.init_app(app)
connector = Connector(app)


@app.route('/')
def index():
    return connector.documentate()


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return connector.select_users()
    if request.method == 'POST' and request.headers['Content-Type'] == 'application/json':
        return connector.insert_user(request)


@app.route('/users/<user_name>', methods=['GET', 'PUT'])
def user(user_name):
    if request.method == 'GET':
        return connector.select_user(user_name)
    if request.method == 'PUT' and request.headers['Content-Type'] == 'application/json':
        return connector.update_user(user_name, request)


@app.route('/users/<user_name>/<secret_token>', methods=['DELETE'])
def user_delete(user_name, secret_token):
    if request.method == 'DELETE':
        return connector.delete_user(user_name, secret_token)


@app.route('/calls', methods=['GET', 'POST'])
def calls():
    if request.method == 'GET':
        return connector.select_calls()
    if request.method == 'POST' and request.headers['Content-Type'] == 'application/json':
        return connector.insert_call(request)


@app.route('/calls/<int:call_id>', methods=['GET', 'PUT'])
def call(call_id):
    if request.method == 'GET':
        return connector.select_call(call_id)
    if request.method == 'PUT' and request.headers['Content-Type'] == 'application/json':
        return connector.update_call(call_id, request)


@app.route('/calls/<int:call_id>/<secret_token>', methods=['DELETE'])
def delete_call(call_id, secret_token):
    if request.method == 'DELETE':
        return connector.delete_call(call_id, secret_token)


@app.route('/tarrifs', methods=['GET', 'POST'])
def tarrifs():
    if request.method == 'GET':
        return connector.select_tarrifs()
    if request.method == 'POST' and request.headers['Content-Type'] == 'application/json':
        return connector.insert_tarrif(request)


@app.route('/tarrifs/<tarrif_name>', methods=['GET', 'PUT'])
def tarrif(tarrif_name):
    if request.method == 'GET':
        return connector.select_tarrif(tarrif_name)
    if request.method == 'PUT' and request.headers['Content-Type'] == 'application/json':
        return connector.update_tarrif(tarrif_name, request)

@app.route('/tarrifs/<tarrif_name>/<secret_token>', methods=['DELETE'])
def delete_tarrif(tarrif_name, secret_token):
    if request.method == 'DELETE':
        return connector.delete_tarrif(tarrif_name, secret_token)

@app.route('/operators', methods=['GET', 'POST'])
def operators():
    if request.method == 'GET':
        return connector.select_operators()
    if request.method == 'POST' and request.headers['Content-Type'] == 'application/json':
        return connector.insert_operator(request)


@app.route('/operators/<operator_name>', methods=['GET', 'PUT'])
def operator(operator_name):
    if request.method == 'GET':
        return connector.select_operator(operator_name)
    if request.method == 'PUT' and request.headers['Content-Type'] == 'application/json':
        return connector.update_operator(operator_name, request)


@app.route('/operators/<operator_name>/<secret_token>', methods=['DELETE'])
def delete_operator(operator_name, secret_token):
    if request.method == 'DELETE':
        return connector.delete_operator(operator_name, secret_token)