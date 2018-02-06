import unittest
from collections import OrderedDict
from flask import json

from tests.tests import ApiTestCase


class TarrifTestCase(ApiTestCase):
    def setUp(self):
        super(self.__class__, self).setUp()
        self.tarrif1 = {u'operator_id': 1, u'name': u'tarrif1', u'cost_per_minute': 0.20}

        self.tarrif2 = {u'operator_id': 1, u'name': u'tarrif2', u'cost_per_minute': 0.38}

        self.token = 'SecretToken'

    def test_empty_db(self):
        resp = self.app.get('/tarrifs')
        self.assertEqual(0, len(json.loads(resp.data)))

    def test_get_tarrifs(self):
        resp = self.app.get('/tarrifs')
        self.assertEqual(0, len(json.loads(resp.data)))
        send_data = self.tarrif1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/tarrifs', send_data)

        resp = self.app.get('/tarrifs')
        self.assertEqual(1, len(json.loads(resp.data)))

        send_data = self.tarrif2
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/tarrifs', send_data)

        resp = self.app.get('/tarrifs')
        self.assertEqual(2, len(json.loads(resp.data)))

    def test_post_tarrif(self):
        send_data = self.tarrif1
        send_data['secret'] = self.token
        resp = self.send_request(self.app.post, '/tarrifs', send_data)
        del send_data['secret']
        send_data['id'] = 1
        self.assertEqual(send_data, json.loads(resp.data)[0])
        send_data = self.tarrif2
        send_data['secret'] = self.token
        resp = self.send_request(self.app.post, '/tarrifs', send_data)
        send_data[u'id'] = 2
        del send_data['secret']
        self.assertEqual(send_data, json.loads(resp.data)[0])

    def test_post_tarrif_not_unique_constraint(self):
        send_data = self.tarrif1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/tarrifs', send_data)
        send_data = self.tarrif2
        send_data[u'name'] = self.tarrif1[u'name']
        send_data['secret'] = self.token
        resp = self.send_request(self.app.post, '/tarrifs', send_data)
        self.assertEqual("400 BAD REQUEST", resp.status)

    def test_post_tarrif_not_null_constraint(self):
        send_data = self.tarrif1
        del send_data[u'name']
        send_data['secret'] = self.token
        resp = self.send_request(self.app.post, '/tarrifs', send_data)
        self.assertEqual("400 BAD REQUEST", resp.status)

    def test_post_tarrif_unallowable_(self):
        send_data = self.tarrif1
        send_data[u'price'] = 1500
        send_data['secret'] = self.token
        resp = self.send_request(self.app.post, '/tarrifs', send_data)
        self.assertEqual("400 BAD REQUEST", resp.status)

    def test_post_tarrif_empty_data(self):
        resp = self.app.post('/tarrifs', content_type='application/json')
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_get_tarrif(self):
        send_data = self.tarrif1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/tarrifs', send_data)
        del send_data['secret']
        send_data[u'id'] = 1
        resp = self.app.get('/tarrifs/tarrif1')
        resp = OrderedDict((json.loads(resp.data)[0]))
        self.assertEqual(send_data, resp)

    def test_get_tarrif__when_tarrif_does_not_exist(self):
        resp = self.app.get('/tarrifs/not_existing_tarrif')
        self.assertEqual(0, len(json.loads(resp.data)))

    def test_put_tarrif(self):
        send_data = self.tarrif1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/tarrifs', send_data)
        send_data[u'name'] = u'smthname'
        send_data[u'id'] = 1
        resp = self.send_request(self.app.put, '/tarrifs/tarrif1', send_data)
        del send_data['secret']
        self.assertEqual(send_data, json.loads(resp.data)[0])

    def test_put_tarrif_when_tarrif_does_not_exist(self):
        send_data = self.tarrif1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/tarrifs', send_data)
        del send_data['secret']
        resp = self.send_request(self.app.put, 'tarrifs/not_existing_tarrif', {'secret': self.token, 'name': 'name'})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_put_tarrif_empty_data(self):
        send_data = self.tarrif1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/tarrifs', send_data)
        del send_data['secret']
        resp = self.send_request(self.app.put, 'tarrifs/tarrif1', {'secret': self.token})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_put_tarrif_unique_constraint(self):
        send_data = self.tarrif1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/tarrifs', send_data)
        send_data = self.tarrif2
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/tarrifs', send_data)
        del send_data['secret']
        resp = self.send_request(self.app.put, 'tarrifs/tarrif2',
                                 {'secret': self.token, u'name': self.tarrif1['name']})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_put_tarrif_not_null_constraint(self):
        send_data = self.tarrif1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/tarrifs', send_data)
        del send_data['secret']
        resp = self.send_request(self.app.put, '/tarrifs/tarrif1', {'secret': self.token, u'name': None})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_put_tarrif_unallowable_key(self):
        send_data = self.tarrif1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/tarrifs', send_data)
        del send_data['secret']
        resp = self.send_request(self.app.put, '/tarrifs/tarrif1', {'secret': self.token, u'price': u'1231231'})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_delete_tarrif(self):
        send_data = self.tarrif1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/tarrifs', send_data)
        send_data = self.tarrif2
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/tarrifs', send_data)
        self.app.delete('/tarrifs/tarrif1/{}'.format(self.token))
        resp = self.app.get('/tarrifs')
        self.assertEqual(len(json.loads(resp.data)), 1)
        self.app.delete('/tarrifs/tarrif2/{}'.format(self.token))
        resp = self.app.get('/tarrifs')
        self.assertEqual(len(json.loads(resp.data)), 0)

    def test_delete_tarrif_when_tarrif_does_not_exist(self):
        send_data = self.tarrif1
        send_data['secret'] = self.token
        self.send_request(self.app.post, 'tarrifs', send_data)
        self.app.delete('/tarrifs/not_existing_tarrif/{}'.format(self.token))
        resp = self.app.get('/tarrifs')
        self.assertEqual(len(json.loads(resp.data)), 1)