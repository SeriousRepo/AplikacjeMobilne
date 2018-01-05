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
	if request.method == 'POST':
		login = raw_input('Type login') 
		password = raw_input('Type password')
		phone_number = raw_input('Type phone number')
		email = raw_input('Type email')

		insert_user(login, password, phone_number, email)
		return "stworzono\n"

@app.route('/users/<user_name>', methods=['GET', 'PUT', 'DELETE'])
def user(user_name):
	if request.method == 'GET':
		return select_user(user_name) 
	if request.method == 'PUT':
		return edate_user(user_name) 
	if request.method == 'DELETE':
		return delete_user(user_name)

@app.route('/calls', methods=['GET', 'POST'])
def calls():
	return 'elo\n'

@app.route('/calls/<int:call_id>', methods=['GET', 'PUT', 'DELETE'])
def call(callId):
	return 'elo\n'

@app.route('/tarrifs', methods=['GET', 'POST'])
def tarrifs():
	return 'elo\n'

@app.route('/tarrifs/<int:tarrifId>', methods=['GET', 'PUT', 'DELETE'])
def tarrif(tarrifId):
	return 'elo\n'

@app.route('/operators', methods=['GET', 'POST'])
def operators():
	return 'elo\n'

@app.route('/operators/<int:operatorId>', methods=['GET', 'PUT', 'DELETE'])
def operator(operatorId):
	return 'elo\n'
