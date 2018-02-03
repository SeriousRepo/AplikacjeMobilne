import unittest
from collections import OrderedDict
from flask import json

from tests.tests import ApiTestCase


class TarrifTestCase(ApiTestCase):
    def setUp(self):
        super(self.__class__, self).setUp()
        self.tarrif1 = {u'operator_id': 1, u'name': u'tarrif1', u'cost_per_minute': 0.20}

        self.tarrif2 = {u'operator_id': 1, u'name': u'tarrif2', u'cost_per_minute': 0.38}

    def test_empty_db(self):
        resp = self.app.get('/tarrifs')
        self.assertEqual(0, len(json.loads(resp.data)))

    def test_get_tarrifs(self):
        resp = self.app.get('/tarrifs')
        self.assertEqual(0, len(json.loads(resp.data)))

        self.send_request(self.app.post, '/tarrifs', self.tarrif1)

        resp = self.app.get('/tarrifs')
        self.assertEqual(1, len(json.loads(resp.data)))

        self.send_request(self.app.post, '/tarrifs', self.tarrif2)

        resp = self.app.get('/tarrifs')
        self.assertEqual(2, len(json.loads(resp.data)))

    def test_post_tarrif(self):
        send_data = self.tarrif1
        resp = self.send_request(self.app.post, '/tarrifs', send_data)
        send_data[u'id'] = 1
        self.assertEqual(send_data, json.loads(resp.data)[0])
        send_data = self.tarrif2
        resp = self.send_request(self.app.post, '/tarrifs', send_data)
        send_data[u'id'] = 2
        self.assertEqual(send_data, json.loads(resp.data)[0])

    def test_post_tarrif_not_unique_constraint(self):
        send_data = self.tarrif1
        self.send_request(self.app.post, '/tarrifs', send_data)
        send_data = self.tarrif2
        send_data[u'name'] = self.tarrif1[u'name']
        resp = self.send_request(self.app.post, '/tarrifs', send_data)
        self.assertEqual("400 BAD REQUEST", resp.status)

    def test_post_tarrif_not_null_constraint(self):
        send_data = self.tarrif1
        del send_data[u'operator_id']
        resp = self.send_request(self.app.post, '/tarrifs', send_data)
        self.assertEqual("400 BAD REQUEST", resp.status)

    def test_post_tarrif_unallowable_(self):
        send_data = self.tarrif1
        send_data[u'price'] = 1500
        resp = self.send_request(self.app.post, '/tarrifs', send_data)
        self.assertEqual("400 BAD REQUEST", resp.status)

    def test_post_tarrif_empty_data(self):
        resp = self.app.post('/tarrifs', content_type='application/json')
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_get_tarrif(self):
        send_data = self.tarrif1
        self.send_request(self.app.post, '/tarrifs', send_data)
        send_data[u'id'] = 1
        resp = self.app.get('/tarrifs/tarrif1')
        resp = OrderedDict((json.loads(resp.data)[0]))
        self.assertEqual(send_data, resp)

    def test_get_tarrif__when_tarrif_does_not_exist(self):
        resp = self.app.get('/tarrifs/not_existing_tarrif')
        self.assertEqual(0, len(json.loads(resp.data)))

    def test_put_tarrif(self):
        send_data = self.tarrif1
        self.send_request(self.app.post, '/tarrifs', send_data)
        send_data[u'cost_per_minute'] = 0.15
        send_data[u'id'] = 1
        resp = self.send_request(self.app.put, '/tarrifs/tarrif1', send_data)
        self.assertEqual(send_data, json.loads(resp.data)[0])

    def test_put_tarrif_when_tarrif_does_not_exist(self):
        send_data = self.tarrif1
        self.send_request(self.app.post, '/tarrifs', send_data)
        resp = self.send_request(self.app.put, 'tarrifs/not_existing_tarrif', {u'name': u'tarrifname'})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_put_tarrif_empty_data(self):
        send_data = self.tarrif1
        self.send_request(self.app.post, '/tarrifs', send_data)
        resp = self.send_request(self.app.put, 'tarrifs/tarrif1', {})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_put_tarrif_unique_constraint(self):
        send_data = self.tarrif1
        self.send_request(self.app.post, '/tarrifs', send_data)
        send_data = self.tarrif2
        self.send_request(self.app.post, '/tarrifs', send_data)
        resp = self.send_request(self.app.put, 'tarrifs/tarrif2', {u'name': u'tarrif1'})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_put_tarrif_not_null_constraint(self):
        send_data = self.tarrif1
        self.send_request(self.app.post, '/tarrifs', send_data)
        resp = self.send_request(self.app.put, '/tarrifs/tarrif1', {u'name': None})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_put_tarrif_unallowable_key(self):
        send_data = self.tarrif1
        self.send_request(self.app.post, '/tarrifs', send_data)
        resp = self.send_request(self.app.put, '/tarrifs/tarrif1', {u'price': u'1231231'})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_delete_tarrif(self):
        self.send_request(self.app.post, '/tarrifs', self.tarrif1)
        self.send_request(self.app.post, '/tarrifs', self.tarrif2)
        self.app.delete('/tarrifs/tarrif1')
        resp = self.app.get('/tarrifs')
        self.assertEqual(len(json.loads(resp.data)), 1)
        self.app.delete('/tarrifs/tarrif2')
        resp = self.app.get('/tarrifs')
        self.assertEqual(len(json.loads(resp.data)), 0)

    def test_delete_tarrif_when_tarrif_does_not_exist(self):
        self.send_request(self.app.post, 'tarrifs', self.tarrif1)
        self.app.delete('/tarrifs/not_existing_tarrif')
        resp = self.app.get('/tarrifs')
        self.assertEqual(len(json.loads(resp.data)), 1)


if __name__ == '__main__':
    unittest.main()