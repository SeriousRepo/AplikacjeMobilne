import sqlite3
from flask import g, Response
from src.utils import convert_to_dict, add_quote_to_str
import json


class Connector:
    def __init__(self, app):
        self.app = app

    def connect_db(self):
        conection = sqlite3.connect(self.app.config['DATABASE'])
        conection.row_factory = sqlite3.Row
        return conection

    def get_db(self):
        if not hasattr(g, 'sqlite_db'):
           g.sqlite_db = self.connect_db()
        return g.sqlite_db

    def init_db(self):
        db = self.get_db()
        with self.app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

    def documentate(self):
        return "Here will be documentation ;)\n"

    def select_users(self):
        try:
            with self.connect_db() as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM User")
                data = convert_to_dict(cur)
            resp = Response(json.dumps(data), status=200, mimetype='application/json'),
        except Exception as e:
            data = '"message": "{}"'.format(e.args[0])
            resp = Response(data, status=400, mimetype='application/json')
        return resp

    def insert_user(self, request):
        resp = self.check_secret_token(request)
        if resp != None:
            return resp
        request_dict = request.get_json()
        del request_dict['secret']
        params = ','.join("{}".format(x) for x in request_dict)
        values = ','.join("{}".format(add_quote_to_str(request_dict[x])) for x in request_dict)
        try:
            with self.connect_db() as con:
                cur = con.cursor()
                cur.execute("INSERT INTO User ({}) VALUES ({});".format(params, values))
                idx = cur.lastrowid
                cur.execute("SELECT * FROM User WHERE id=?;", (idx,))
                data = convert_to_dict(cur)
                con.commit()
            resp = Response(json.dumps(data), status=201, mimetype='application/json')
        except Exception as e:
            data = '"message": "{}"'.format(e.args[0])
            resp = Response(data, status=400, mimetype='application/json')
        return resp

    def select_user(self, username):
        try:
            with self.connect_db() as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM User WHERE login=?", (username,))
                data = convert_to_dict(cur)
            resp = Response(json.dumps(data), status=200, mimetype='application/json')
        except Exception as e:
            data = '"message": "{}"'.format(e.args[0])
            resp = Response(data, status=400, mimetype='application/json')
        return resp

    def update_user(self, username, request):
        request_dict = request.get_json()
        if self.login(request) != None:
            if self.check_secret_token(request) != None:
                return Response('{"message": "Not autorized"}', status=401, mimetype='application/error')
        if 'last_login' in request_dict:
            del request_dict['last_login']
        if 'last_password' in request_dict:
            del request_dict['last_password']
        if 'secret' in request_dict:
            del request_dict['secret']
        params = ','.join("{}={}".format(x, add_quote_to_str(request_dict[x])) for x in request_dict)
        query = ("UPDATE User SET {} WHERE login='{}';").format(params, username)
        try:
            with self.connect_db() as con:
                cur = con.cursor()
                cur.execute("SELECT id FROM User WHERE login=?", (username,))
                idx = cur.fetchone()[0]
                cur.execute(query)
                cur.execute("SELECT * FROM User WHERE id=?", (idx,))
                data = convert_to_dict(cur)
            resp = Response(json.dumps(data), status=200, mimetype='application/json')
        except Exception as e:
            data = '"message": "{}"'.format(e.args[0])
            resp = Response(data, status=400, mimetype='application/json')
        return resp

    def delete_user(self, username, token):
        if token != 'SecretToken':
            return Response('{"message": You need to provide secret token for this functionality"}', status=401, mimetype='application/json')
        try:
            with self.connect_db() as con:
                cur = con.cursor()
                cur.execute("DELETE FROM User WHERE login=?", (username,))
                con.commit()
            resp = Response(status=200, mimetype='application/json')
        except Exception as e:
            data = '"message": "{}"'.format(e.args[0])
            resp = Response(data, status=400, mimetype='application/json')
        return resp

    def select_calls(self):
        try:
            with self.connect_db() as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Call")
                data = convert_to_dict(cur)
            resp = Response(json.dumps(data), status=200, mimetype='application/json')
        except Exception as e:
            data = '"message": "{}"'.format(e.args[0])
            resp = Response(data, status=400, mimetype='application/json')
        return resp

    def insert_call(self, request):
        resp = self.check_secret_token(request)
        if resp != None:
            return resp
        request_dict = request.get_json()
        del request_dict['secret']
        params = ','.join("{}".format(x) for x in request_dict)
        values = ','.join("{}".format(add_quote_to_str(request_dict[x])) for x in request_dict)
        try:
            with self.connect_db() as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Call ({}) VALUES ({});".format(params, values))
                idx = cur.lastrowid
                cur.execute("SELECT * FROM Call WHERE id=?;", (idx,))
                data = convert_to_dict(cur)
                con.commit()
            resp = Response(json.dumps(data), status=201, mimetype='application/json')
        except Exception as e:
            data = '"message": "{}"'.format(e.args[0])
            resp = Response(data, status=400, mimetype='application/json')
        return resp

    def select_call(self, call_id):
        try:
            with self.connect_db() as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Call WHERE id=?", (call_id,))
                data = convert_to_dict(cur)
            resp = Response(json.dumps(data), status=200, mimetype='application/json')
        except Exception as e:
            data = '"message": "{}"'.format(e.args[0])
            resp = Response(data, status=400, mimetype='application/json')
        return resp

    def update_call(self, call_id, request):
        resp = self.check_secret_token(request)
        if resp != None:
            return resp
        request_dict = request.get_json()
        del request_dict['secret']
        params = ','.join("{}={}".format(x, add_quote_to_str(request_dict[x])) for x in request_dict)
        query = ("UPDATE Call SET {} WHERE id='{}';").format(params, call_id)
        try:
            with self.connect_db() as con:
                cur = con.cursor()
                cur.execute("SELECT id FROM Call WHERE id=?", (call_id,))
                idx = cur.fetchone()[0]
                cur.execute(query)
                cur.execute("SELECT * FROM Call WHERE id=?", (idx,))
                data = convert_to_dict(cur)
            resp = Response(json.dumps(data), status=200, mimetype='application/json')
        except Exception as e:
            data = '"message": "{}"'.format(e.args[0])
            resp = Response(data, status=400, mimetype='application/json')
        return resp

    def delete_call(self, call_id, token):
        if token != 'SecretToken':
            return Response('{"message": You need to provide secret token for this functionality"}', status=401, mimetype='application/json')
        try:
            with self.connect_db() as con:
                cur = con.cursor()
                cur.execute("DELETE FROM Call WHERE id=?", (call_id,))
                con.commit()
            resp = Response(status=200, mimetype='application/json')
        except Exception as e:
            data = '"message": "{}"'.format(e.args[0])
            resp = Response(data, status=400, mimetype='application/json')
        return resp

    def select_tarrifs(self):
        try:
            with self.connect_db() as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Tarrif")
                data = convert_to_dict(cur)
            resp = Response(json.dumps(data), status=200, mimetype='application/json')
        except Exception as e:
            data = '"message": "{}"'.format(e.args[0])
            resp = Response(data, status=400, mimetype='application/json')
        return resp

    def insert_tarrif(self, request):
        resp = self.check_secret_token(request)
        if resp != None:
            return resp
        request_dict = request.get_json()
        del request_dict['secret']
        params = ','.join("{}".format(x) for x in request_dict)
        values = ','.join("{}".format(add_quote_to_str(request_dict[x])) for x in request_dict)
        try:
            with self.connect_db() as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Tarrif ({}) VALUES ({});".format(params, values))
                idx = cur.lastrowid
                cur.execute("SELECT * FROM Tarrif WHERE id=?;", (idx,))
                data = convert_to_dict(cur)
                con.commit()
            resp = Response(json.dumps(data), status=201, mimetype='application/json')
        except Exception as e:
            data = '"message": "{}"'.format(e.args[0])
            resp = Response(data, status=400, mimetype='application/json')
        return resp

    def select_tarrif(self, tarrif_name):
        try:
            with self.connect_db() as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Tarrif WHERE name=?", (tarrif_name,))
                data = convert_to_dict(cur)
            resp = Response(json.dumps(data), status=200, mimetype='application/json')
        except Exception as e:
            data = '"message": "{}"'.format(e.args[0])
            resp = Response(data, status=400, mimetype='application/json')
        return resp

    def update_tarrif(self, tarrif_name, request):
        resp = self.check_secret_token(request)
        if resp != None:
            return resp
        request_dict = request.get_json()
        del request_dict['secret']
        params = ','.join("{}={}".format(x, add_quote_to_str(request_dict[x])) for x in request_dict)
        query = ("UPDATE Tarrif SET {} WHERE name='{}';").format(params, tarrif_name)
        try:
            with self.connect_db() as con:
                cur = con.cursor()
                cur.execute("SELECT id FROM Tarrif WHERE name=?", (tarrif_name,))
                idx = cur.fetchone()[0]
                cur.execute(query)
                cur.execute("SELECT * FROM Tarrif WHERE id=?", (idx,))
                data = convert_to_dict(cur)
            resp = Response(json.dumps(data), status=200, mimetype='application/json')
        except Exception as e:
            data = '"message": "{}"'.format(e.args[0])
            resp = Response(data, status=400, mimetype='application/json')
        return resp

    def delete_tarrif(self, tarrif_name, token):
        if token != 'SecretToken':
            return Response('{"message": You need to provide secret token for this functionality"}', status=401, mimetype='application/json')
        try:
            with self.connect_db() as con:
                cur = con.cursor()
                cur.execute("DELETE FROM Tarrif WHERE name=?", (tarrif_name,))
                con.commit()
            resp = Response(status=200, mimetype='application/json')
        except Exception as e:
            data = '"message": "{}"'.format(e.args[0])
            resp = Response(data, status=400, mimetype='application/json')
        return resp

    def select_operators(self):
        try:
            with self.connect_db() as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Operator")
                data = convert_to_dict(cur)
            resp = Response(json.dumps(data), status=200, mimetype='application/json')
        except Exception as e:
            data = '"message": "{}"'.format(e.args[0])
            resp = Response(data, status=400, mimetype='application/json')
        return resp

    def insert_operator(self, request):
        resp = self.check_secret_token(request)
        if resp != None:
            return resp
        request_dict = request.get_json()
        del request_dict['secret']
        params = ','.join("{}".format(x) for x in request_dict)
        values = ','.join("{}".format(add_quote_to_str(request_dict[x])) for x in request_dict)
        try:
            with self.connect_db() as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Operator ({}) VALUES ({});".format(params, values))
                idx = cur.lastrowid
                cur.execute("SELECT * FROM Operator WHERE id=?;", (idx,))
                data = convert_to_dict(cur)
                con.commit()
            resp = Response(json.dumps(data), status=201, mimetype='application/json')
        except Exception as e:
            data = '"message": "{}"'.format(e.args[0])
            resp = Response(data, status=400, mimetype='application/json')
        return resp

    def select_operator(self, operator_name):
        try:
            with self.connect_db() as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Operator WHERE name=?", (operator_name,))
                data = convert_to_dict(cur)
            resp = Response(json.dumps(data), status=200, mimetype='application/json')
        except Exception as e:
            data = '"message": "{}"'.format(e.args[0])
            resp = Response(data, status=400, mimetype='application/json')
        return resp

    def update_operator(self, operator_name, request):
        resp = self.check_secret_token(request)
        if resp != None:
            return resp
        request_dict = request.get_json()
        del request_dict['secret']
        params = ','.join("{}={}".format(x, add_quote_to_str(request_dict[x])) for x in request_dict)
        query = ("UPDATE Operator SET {} WHERE name='{}';").format(params, operator_name)
        try:
            with self.connect_db() as con:
                cur = con.cursor()
                cur.execute("SELECT id FROM Operator WHERE name=?", (operator_name,))
                idx = cur.fetchone()[0]
                cur.execute(query)
                cur.execute("SELECT * FROM Operator WHERE id=?", (idx,))
                data = convert_to_dict(cur)
            resp = Response(json.dumps(data), status=200, mimetype='application/json')
        except Exception as e:
            data = '"message": "{}"'.format(e.args[0])
            resp = Response(data, status=400, mimetype='application/json')
        return resp

    def delete_operator(self, operator_name, token):
        if token != 'SecretToken':
            return Response('{"message": You need to provide secret token for this functionality"}', status=401, mimetype='application/json')
        try:
            with self.connect_db() as con:
                cur = con.cursor()
                cur.execute("DELETE FROM Operator WHERE name=?", (operator_name,))
                con.commit()
            resp = Response(status=200, mimetype='application/json')
        except Exception as e:
            data = '"message": "{}"'.format(e.args[0])
            resp = Response(data, status=400, mimetype='application/json')
        return resp

    def login(self, request):
        request_dict = request.get_json()
        if 'last_login' not in request_dict or 'last_password' not in request_dict:
            data = '{"message": "you need to provide login with password or secret token"}'
            return Response(data, status=401, mimetype='application/json')
        given_login = request_dict['last_login']
        given_password = request_dict['last_password']
        users_data = self.get_users()
        single_user = None
        for usr in users_data:
            if given_login in usr['login']:
                single_user = usr
        if single_user == None:
            data = '{"message": "Wrong username"}'
            return Response(data, status=401, mimetype='application/json')
        if given_password == single_user['password']:
            return None
        else:
            data = '{"message": "Wrong password"}'
            status = 401
            return Response(data, status=status, mimetype='application/json')

    def get_users(self):
        try:
            with self.connect_db() as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM User")
                data = convert_to_dict(cur)
            return data
        except Exception as e:
            return

    def check_secret_token(self, request):
        data = request.get_json()
        if 'secret' in data:
            if data['secret'] == 'SecretToken':
                return None
        return Response('{"message": You need to provide secret token for this functionality"}', status=401, mimetype='application/json')
