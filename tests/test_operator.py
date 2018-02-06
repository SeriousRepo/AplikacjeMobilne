from collections import OrderedDict
from flask import json

from tests.tests import ApiTestCase


class OperatorTestCase(ApiTestCase):
    def setUp(self):
        super(self.__class__, self).setUp()
        self.operator1 = {u'name': u'operator1'}

        self.operator2 = {u'name': u'operator2'}

        self.token = 'SecretToken'

    def test_empty_db(self):
        resp = self.app.get('/operators')
        self.assertEqual(0, len(json.loads(resp.data)))

    def test_get_operators(self):
        resp = self.app.get('/operators')
        self.assertEqual(0, len(json.loads(resp.data)))
        send_data = self.operator1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/operators', send_data)

        resp = self.app.get('/operators')
        self.assertEqual(1, len(json.loads(resp.data)))

        send_data = self.operator2
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/operators', send_data)

        resp = self.app.get('/operators')
        self.assertEqual(2, len(json.loads(resp.data)))

    def test_post_operator(self):
        send_data = self.operator1
        send_data['secret'] = self.token
        resp = self.send_request(self.app.post, '/operators', send_data)
        del send_data['secret']
        send_data['id'] = 1
        self.assertEqual(send_data, json.loads(resp.data)[0])
        send_data = self.operator2
        send_data['secret'] = self.token
        resp = self.send_request(self.app.post, '/operators', send_data)
        send_data[u'id'] = 2
        del send_data['secret']
        self.assertEqual(send_data, json.loads(resp.data)[0])

    def test_post_operator_not_unique_constraint(self):
        send_data = self.operator1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/operators', send_data)
        send_data = self.operator2
        send_data[u'name'] = self.operator1[u'name']
        send_data['secret'] = self.token
        resp = self.send_request(self.app.post, '/operators', send_data)
        self.assertEqual("400 BAD REQUEST", resp.status)

    def test_post_operator_not_null_constraint(self):
        send_data = self.operator1
        del send_data[u'name']
        send_data['secret'] = self.token
        resp = self.send_request(self.app.post, '/operators', send_data)
        self.assertEqual("400 BAD REQUEST", resp.status)

    def test_post_operator_unallowable_(self):
        send_data = self.operator1
        send_data[u'price'] = 1500
        send_data['secret'] = self.token
        resp = self.send_request(self.app.post, '/operators', send_data)
        self.assertEqual("400 BAD REQUEST", resp.status)

    def test_post_operator_empty_data(self):
        resp = self.app.post('/operators', content_type='application/json')
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_get_operator(self):
        send_data = self.operator1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/operators', send_data)
        del send_data['secret']
        send_data[u'id'] = 1
        resp = self.app.get('/operators/operator1')
        resp = OrderedDict((json.loads(resp.data)[0]))
        self.assertEqual(send_data, resp)

    def test_get_operator__when_operator_does_not_exist(self):
        resp = self.app.get('/operators/not_existing_operator')
        self.assertEqual(0, len(json.loads(resp.data)))

    def test_put_operator(self):
        send_data = self.operator1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/operators', send_data)
        send_data[u'name'] = u'smthname'
        send_data[u'id'] = 1
        resp = self.send_request(self.app.put, '/operators/operator1', send_data)
        del send_data['secret']
        self.assertEqual(send_data, json.loads(resp.data)[0])

    def test_put_operator_when_operator_does_not_exist(self):
        send_data = self.operator1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/operators', send_data)
        del send_data['secret']
        resp = self.send_request(self.app.put, 'operators/not_existing_operator', {'secret': self.token, 'name': 'name'})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_put_operator_empty_data(self):
        send_data = self.operator1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/operators', send_data)
        del send_data['secret']
        resp = self.send_request(self.app.put, 'operators/operator1', {'secret': self.token})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_put_operator_unique_constraint(self):
        send_data = self.operator1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/operators', send_data)
        send_data = self.operator2
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/operators', send_data)
        del send_data['secret']
        resp = self.send_request(self.app.put, 'operators/operator2',
                                 {'secret': self.token, u'name': self.operator1['name']})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_put_operator_not_null_constraint(self):
        send_data = self.operator1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/operators', send_data)
        del send_data['secret']
        resp = self.send_request(self.app.put, '/operators/operator1', {'secret': self.token, u'name': None})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_put_operator_unallowable_key(self):
        send_data = self.operator1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/operators', send_data)
        del send_data['secret']
        resp = self.send_request(self.app.put, '/operators/operator1', {'secret': self.token, u'price': u'1231231'})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_delete_operator(self):
        send_data = self.operator1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/operators', send_data)
        send_data = self.operator2
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/operators', send_data)
        self.app.delete('/operators/operator1/{}'.format(self.token))
        resp = self.app.get('/operators')
        self.assertEqual(len(json.loads(resp.data)), 1)
        self.app.delete('/operators/operator2/{}'.format(self.token))
        resp = self.app.get('/operators')
        self.assertEqual(len(json.loads(resp.data)), 0)

    def test_delete_operator_when_operator_does_not_exist(self):
        send_data = self.operator1
        send_data['secret'] = self.token
        self.send_request(self.app.post, 'operators', send_data)
        self.app.delete('/operators/not_existing_operator/{}'.format(self.token))
        resp = self.app.get('/operators')
        self.assertEqual(len(json.loads(resp.data)), 1)