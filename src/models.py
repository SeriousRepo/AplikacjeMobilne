import sqlite3 as sql
import json
from flask import Response, request

FILEPATH = "src/database.db"

def convert_to_dict(cur):
	dictio = [ dict(line) for line in [ zip([ column[0] for column in cur.description ], row) for row in cur.fetchall() ] ]
	return dictio	

def param_handler(param_dict, param_tuple):
	product = []
	for param in param_tuple:
		if param in param_dict:
			product.append(param_dict[param])
		else:
			product.append(None)
	return tuple(product)

def documentate():
	return "Here will be documentation ;)\n"

def select_users():
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.execute("SELECT * FROM User")
		data = convert_to_dict(cur)
	resp = Response(json.dumps(data), status=200, mimetype='application/json')
	return resp
			
def insert_user(request):
	request_dict = request.get_json()
	possible_params = ('login','password', 'phone_number', 'email', 'name', 'surname', 'birth_date', 'sex')
	proper_params = param_handler(request_dict, possible_params)
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.executemany("INSERT INTO User ({}) VALUES (?,?,?,?,?,?,?,?);".format(','.join(str(x) for x in possible_params)), (proper_params,))
		idx = cur.lastrowid
		con.commit()
	data = {'id': idx}
	data.update(dict(zip(possible_params, proper_params)))
	resp = Response(json.dumps(data), status=201, mimetype='application/json')
	resp.headers['Message'] = "User {} was successfully added".format(data['login'])
	return resp

def select_user(username):
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.execute("SELECT * FROM User WHERE login=?", (username,))
		data = convert_to_dict(cur)
	resp = Response(json.dumps(data), status=200, mimetype='application/json')
	return resp

def update_user(username, request):
	request_dict = request.get_json()
	values_tuple = tuple(request_dict.values())
	params = ','.join(str(x)+'=?' for x in request_dict) 
	query = ("UPDATE User SET {} WHERE login=\"{}\"".format(params, username))
	print(query)
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.execute(query)
		#data = select_user(username)
		#resp = Response
	return "smth"

def delete_user(username):
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.execute("DELETE FROM User WHERE EXISTS(SELECT * FROM User WHERE login=?) AND login=?", (username, username))
		con.commit()
	resp = Response(status=200, mimetype='application/json')
	resp.headers['Message'] = "User {} was successfully deleted".format(username) 
	return resp

