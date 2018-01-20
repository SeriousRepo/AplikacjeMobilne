from src import app
from flask import Flask
from flask import request
from models import *

@app.route('/')
def index():
	return documentate()

@app.route('/users', methods=['GET', 'POST'])
def users():
	if request.method == 'GET':	
		return select_users()
	if request.method == 'POST' and request.headers['Content-Type'] == 'application/json':
		return insert_user(request)

@app.route('/users/<user_name>', methods=['GET', 'PUT', 'DELETE'])
def user(user_name):
	if request.method == 'GET':
		return select_user(user_name) 
	if request.method == 'PUT' and request.headers['Content-Type'] == 'application/json':
		return update_user(user_name, request) 
	if request.method == 'DELETE':
		return delete_user(user_name)

@app.route('/calls', methods=['GET', 'POST'])
def calls():
	if request.method == 'GET':
		return select_calls()
	if request.method == 'POST' and request.headers['Content-Type'] == 'application/json':
		return insert_call(request)

@app.route('/calls/<int:call_id>', methods=['GET', 'PUT', 'DELETE'])
def call(call_id):
	if request.method == 'GET':
		return select_call(call_id) 
	if request.method == 'PUT' and request.headers['Content-Type'] == 'application/json':
		return update_call(call_id, request) 
	if request.method == 'DELETE':
		return delete_call(call_id)

@app.route('/tarrifs', methods=['GET', 'POST'])
def tarrifs():
	if request.method == 'GET':	
		return select_tarrifs()
	if request.method == 'POST' and request.headers['Content-Type'] == 'application/json':
		return insert_tarrif(request)

@app.route('/tarrifs/<tarrif_name>', methods=['GET', 'PUT', 'DELETE'])
def tarrif(tarrif_name):
	if request.method == 'GET':
		return select_tarrif(tarrif_name) 
	if request.method == 'PUT' and request.headers['Content-Type'] == 'application/json':
		return update_tarrif(tarrif_name, request) 
	if request.method == 'DELETE':
		return delete_tarrif(tarrif_name)

	

@app.route('/operators', methods=['GET', 'POST'])
def operators():
	return 'operators methods\n'

@app.route('/operators/<int:operatorId>', methods=['GET', 'PUT', 'DELETE'])
def operator(operatorId):
	return 'operator methods\n'
