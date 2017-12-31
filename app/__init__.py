from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy

from config import app_config

db = SQLAlchemy()

def create_app(config_name):
	app = Flask(__name__)

	@app.route('/')
	def documentate():
		return "Here will be documentation ;)\n"

	@app.route('/users', methods=['GET', 'POST'])
	def users():
		if request.method == 'GET':
			return 'Users list\n'
		if request.method == 'POST':
			return 'Create user\n'

	@app.route('/users/<int:userId>', methods=['GET', 'PUT', 'DELETE'])
	def user(userId):
		if request.method == 'GET':
			return 'get user %d \n' % userId 
		if request.method == 'PUT':
			return 'put user %d \n' % userId 
		if request.method == 'DELETE':
			return 'delete user %d \n' % userId

	@app.route('/calls', methods=['GET', 'POST'])
	def calls():
		return 'elo\n'

	@app.route('/calls/<int:callId>', methods=['GET', 'PUT', 'DELETE'])
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
		
	return app
