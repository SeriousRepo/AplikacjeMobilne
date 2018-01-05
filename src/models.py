import sqlite3 as sql
import json

FILEPATH = "src/database.db"

def convert_to_json(cur):
	response = [ dict(line) for line in [ zip([ column[0] for column in cur.description ], row) for row in cur.fetchall() ] ]
	return json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))	

def documentate():
	return "Here will be documentation ;)\n"

def select_users():
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.execute("SELECT * FROM User")
		result = convert_to_json(cur)
	return result
			
def insert_user(login, password, phone_number, email):
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.execute("INSERT INTO User (login, password, phone_number, email) VALUES (?,?,?,?)", [login, password, phone_number, email])
		con.commit()

def select_user(username):
	with sql.connect(FILEPATH) as con:
		cur = con.cursor()
		cur.execute("SELECT * FROM User WHERE login=?", [username])
		result = convert_to_json(cur)
	return result

def update_user(username):
	return "\n\n\n\n"

def delete_user(username):
	with sql.connect(FILEPATH) as con:
                cur = con.cursor()
                cur.execute("DELETE FROM User WHERE login=?", [username])
	return "removed\n"

