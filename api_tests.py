import os
import src
import unittest
import tempfile
import sqlite3 as sql
import json
from flask import jsonify

class ApiTestCase(unittest.TestCase):

	def setUp(self):
		#self.db_fd, src.app.config['DATABASE'] = tempfile.mkstemp()
		#src.app.testing = True
		self.app = src.app.test_client()
		#with src.app.app_context():
		#	src.init_db()
	
	def tearDown(self):
		pass
		#os.close(self.db_fd)
		#os.unlink(src.app.config['DATABASE'])

	def test_empty_db(self):
		response = self.app.get('/users')
		self.assertEqual(json.loads(response.data), [])
		response = self.app.get('/calls')
		self.assertEqual(json.loads(response.data), [])
		response = self.app.get('/tarrifs')
		self.assertEqual(json.loads(response.data), [])
		response = self.app.get('/operators')
		self.assertEqual(json.loads(response.data), [])
	
	def test_post_user(self):
		send_data ={u'login':u'login', u'password':u'password', u'phone_number':u'123456789', u'email':u'email@email.email'}   
		response = self.app.post('/users', data=json.dumps(send_data), content_type='application/json')
		send_data[u'birth_date'] = None
		send_data[u'name'] = None
		send_data[u'surname'] = None
		send_data[u'sex'] = None
		send_data[u'id'] = 1
		self.assertEqual(send_data, json.loads(response.data)[0])
	
	def test_update_user(self):
		send_data = {u'password':u'pswd'}
		data = dict(
			login=u'login',
			password=u'pswd', 
			phone_number=u'123456789', 
			email=u'email@email.email', 
			birth_date=None,
			name=None, 	
			surname=None,
			sex=None,
			id=1
		) 	
		response = self.app.put('users/login', data=json.dumps(send_data), content_type='application/json')
		self.assertEqual(data, json.loads(response.data)[0])
#self.assertRaises(sql.IntegrityError,  self.app.post, '/users', data=json.dumps(dict(login='login')), content_type='application/json')

	def test_not_unique_constraint_after_post(self):
		send_data ={u'login':u'login', u'password':u'password', u'phone_number':u'123156789', u'email':u'emaillllll@email.email'}   
		response = self.app.post('/users', data=json.dumps(send_data), content_type='application/json')
		send_data[u'birth_date'] = None
		send_data[u'name'] = None
		send_data[u'surname'] = None
		send_data[u'sex'] = None
		send_data[u'id'] = 1
		self.assertEqual({'messaege':'UNIQUE constraint fault'}, json.loads(response.data)[0])
		
	
if __name__ == '__main__':
	unittest.main()
