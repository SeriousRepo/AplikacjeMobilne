import os
import src
import unittest
import tempfile

class ApiTestCase(unittest.TestCase):

	def setUp(self):
		self.app = src.app.test_client()
		self.app.testing = True

	def tearDown(self):
		pass
		
	def test_empty_db(self):
		response = self.app.get('/users')
		assert b'[]' in response.data
	
	def test_post_user(self):
		response = self.app.post('/users', data=dict(login='login'))
		assert b'[]' in response.data
	

if __name__ == '__main__':
    unittest.main()
