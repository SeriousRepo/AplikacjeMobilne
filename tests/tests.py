import os
import unittest
import tempfile
import json

from src.utils import app
from src.Connector import Connector


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.testing = True
        connector = Connector(app)
        self.app = app.test_client()
        with app.app_context():
            connector.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def choose_keys(self, table, keys):
        product = dict()
        for key in keys:
            product[key] = table[key]
        return product

    def send_request(self, func, route, data):
        return func(route, data=json.dumps(data), content_type='application/json')
