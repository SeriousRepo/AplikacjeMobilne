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

def add_quote_to_str(param):
	if type(param) is unicode:
		param = "'" + param + "'"
	return param

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
	params = ','.join("{}".format(x) for x in request_dict)
	values = ','.join("{}".format(add_quote_to_str(request_dict[x])) for x in request_dict)
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.execute("INSERT INTO User ({}) VALUES ({});".format(params, values))
		idx = cur.lastrowid
		cur.execute("SELECT * FROM User WHERE id=?;", (idx,))
		data = convert_to_dict(cur)
		con.commit()
	resp = Response(json.dumps(data), status=201, mimetype='application/json')
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
	params = ','.join("{}={}".format(x, add_quote_to_str(request_dict[x])) for x in request_dict)
	query = ("UPDATE User SET {} WHERE login='{}';").format(params, username)
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.execute("SELECT id FROM User WHERE login=?", (username,))
		idx = cur.fetchone()[0]
		cur.execute(query)
		cur.execute("SELECT * FROM User WHERE id=?", (idx,))
		data = convert_to_dict(cur)
	resp = Response(json.dumps(data), status=200, mimetype='application/json')
	return resp

def delete_user(username):
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.execute("DELETE FROM User WHERE login=?", (username,))
		con.commit()
	resp = Response(status=200, mimetype='application/json')
	resp.headers['Message'] = "User {} was successfully deleted".format(username) 
	return resp

def select_calls():
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.execute("SELECT * FROM Call")
		data = convert_to_dict(cur)
	resp = Response(json.dumps(data), status=200, mimetype='application/json')
	return resp

def insert_call(request):
	request_dict = request.get_json()
	params = ','.join("{}".format(x) for x in request_dict)
	values = ','.join("{}".format(add_quote_to_str(request_dict[x])) for x in request_dict)
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.execute("INSERT INTO Call ({}) VALUES ({});".format(params, values))
		idx = cur.lastrowid
		cur.execute("SELECT * FROM Call WHERE id=?;", (idx,))
		data = convert_to_dict(cur)
		con.commit()
	resp = Response(json.dumps(data), status=201, mimetype='application/json')
	return resp

def select_call(call_id):
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.execute("SELECT * FROM Call WHERE id=?", (call_id,))
		data = convert_to_dict(cur)
	resp = Response(json.dumps(data), status=200, mimetype='application/json')
	return resp

def update_call(call_id, request):
	request_dict = request.get_json()
	params = ','.join("{}={}".format(x, add_quote_to_str(request_dict[x])) for x in request_dict)
	query = ("UPDATE Call SET {} WHERE id='{}';").format(params, call_id)
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.execute("SELECT id FROM Call WHERE id=?", (call_id,))
		idx = cur.fetchone()[0]
		cur.execute(query)
		cur.execute("SELECT * FROM Call WHERE id=?", (idx,))
		data = convert_to_dict(cur)
	resp = Response(json.dumps(data), status=200, mimetype='application/json')
	return resp

def delete_call(call_id):
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.execute("DELETE FROM Call WHERE id=?", (call_id,))
		con.commit()
	resp = Response(status=200, mimetype='application/json')
	resp.headers['Message'] = "User {} was successfully deleted".format(call_id) 
	return resp

def select_tarrifs():
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.execute("SELECT * FROM Tarrif")
		data = convert_to_dict(cur)
	resp = Response(json.dumps(data), status=200, mimetype='application/json')
	return resp

def insert_tarrif(request):
	request_dict = request.get_json()
	params = ','.join("{}".format(x) for x in request_dict)
	values = ','.join("{}".format(add_quote_to_str(request_dict[x])) for x in request_dict)
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.execute("INSERT INTO Tarrif ({}) VALUES ({});".format(params, values))
		idx = cur.lastrowid
		cur.execute("SELECT * FROM Tarrif WHERE id=?;", (idx,))
		data = convert_to_dict(cur)
		con.commit()
	resp = Response(json.dumps(data), status=201, mimetype='application/json')
	return resp

def select_tarrif(tarrif_name):
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.execute("SELECT * FROM Tarrif WHERE name=?", (tarrif_name,))
		data = convert_to_dict(cur)
	resp = Response(json.dumps(data), status=200, mimetype='application/json')
	return resp

def update_tarrif(tarrif_name, request):
	request_dict = request.get_json()
	params = ','.join("{}={}".format(x, add_quote_to_str(request_dict[x])) for x in request_dict)
	query = ("UPDATE Tarrif SET {} WHERE name='{}';").format(params, tarrif_name)
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.execute("SELECT id FROM Tarrif WHERE name=?", (tarrif_name,))
		idx = cur.fetchone()[0]
		cur.execute(query)
		cur.execute("SELECT * FROM Tarrif WHERE id=?", (idx,))
		data = convert_to_dict(cur)
	resp = Response(json.dumps(data), status=200, mimetype='application/json')
	return resp

def delete_tarrif(tarrif_name):
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.execute("DELETE FROM Tarrif WHERE name=?", (tarrif_name,))
		con.commit()
	resp = Response(status=200, mimetype='application/json')
	resp.headers['Message'] = "User {} was successfully deleted".format(tarrif_name) 
	return resp

def select_operators():
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.execute("SELECT * FROM Operator")
		data = convert_to_dict(cur)
	resp = Response(json.dumps(data), status=200, mimetype='application/json')
	return resp

def insert_operator(request):
	request_dict = request.get_json()
	params = ','.join("{}".format(x) for x in request_dict)
	values = ','.join("{}".format(add_quote_to_str(request_dict[x])) for x in request_dict)
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.execute("INSERT INTO Operator ({}) VALUES ({});".format(params, values))
		idx = cur.lastrowid
		cur.execute("SELECT * FROM Operator WHERE id=?;", (idx,))
		data = convert_to_dict(cur)
		con.commit()
	resp = Response(json.dumps(data), status=201, mimetype='application/json')
	return resp

def select_operator(operator_name):
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.execute("SELECT * FROM Operator WHERE name=?", (operator_name,))
		data = convert_to_dict(cur)
	resp = Response(json.dumps(data), status=200, mimetype='application/json')
	return resp

def update_operator(operator_name, request):
	request_dict = request.get_json()
	params = ','.join("{}={}".format(x, add_quote_to_str(request_dict[x])) for x in request_dict)
	query = ("UPDATE Operator SET {} WHERE name='{}';").format(params, operator_name)
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.execute("SELECT id FROM Operator WHERE name=?", (operator_name,))
		idx = cur.fetchone()[0]
		cur.execute(query)
		cur.execute("SELECT * FROM Operator WHERE id=?", (idx,))
		data = convert_to_dict(cur)
	resp = Response(json.dumps(data), status=200, mimetype='application/json')
	return resp

def delete_operator(operator_name):
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.execute("DELETE FROM Operator WHERE name=?", (operator_name,))
		con.commit()
	resp = Response(status=200, mimetype='application/json')
	resp.headers['Message'] = "User {} was successfully deleted".format(operator_name) 
	return resp

