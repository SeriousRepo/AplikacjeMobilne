from collections import OrderedDict
from flask import json

from tests.tests import ApiTestCase


class CallTestCase(ApiTestCase):
    def setUp(self):
        super(self.__class__, self).setUp()
        self.call1 = {u'user1_id': 1, u'user2_id': 2,
                      u'tarrif_id': 1, u'call_date': u'1111-11-11 11:11:11',
                      u'duration': 15, u'quality': 5}

        self.call2 = {u'user1_id': 1, u'user2_id': 2,
                      u'tarrif_id': 1, u'call_date': u'1111-11-11 22:22:22',
                      u'duration': 35, u'quality': 5}
        self.token = 'SecretToken'

    def test_empty_db(self):
        resp = self.app.get('/calls')
        self.assertEqual(0, len(json.loads(resp.data)))

    def test_get_calls(self):
        resp = self.app.get('/calls')
        self.assertEqual(0, len(json.loads(resp.data)))
        send_data = self.call1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/calls', send_data)

        resp = self.app.get('/calls')
        self.assertEqual(1, len(json.loads(resp.data)))

        send_data = self.call2
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/calls', send_data)

        resp = self.app.get('/calls')
        self.assertEqual(2, len(json.loads(resp.data)))

    def test_post_call(self):
        send_data = self.call1
        send_data['secret'] = self.token
        resp = self.send_request(self.app.post, '/calls', send_data)
        del send_data['secret']
        send_data['id'] = 1
        self.assertEqual(send_data, json.loads(resp.data)[0])
        send_data = self.call2
        send_data['secret'] = self.token
        resp = self.send_request(self.app.post, '/calls', send_data)
        send_data[u'id'] = 2
        del send_data['secret']
        self.assertEqual(send_data, json.loads(resp.data)[0])

    def test_post_call_not_null_constraint(self):
        send_data = self.call1
        del send_data['tarrif_id']
        send_data['secret'] = self.token
        resp = self.send_request(self.app.post, '/calls', send_data)
        self.assertEqual("400 BAD REQUEST", resp.status)

    def test_post_call_check_constraint(self):
        send_data = self.call1
        send_data[u'call_date'] = u'2017-12-12'
        send_data['secret'] = self.token
        resp = self.send_request(self.app.post, '/calls', send_data)
        self.assertEqual("400 BAD REQUEST", resp.status)

    def test_post_call_unallowable_(self):
        send_data = self.call1
        send_data[u'price'] = 1500
        send_data['secret'] = self.token
        resp = self.send_request(self.app.post, '/calls', send_data)
        self.assertEqual("400 BAD REQUEST", resp.status)

    def test_post_call_empty_data(self):
        resp = self.app.post('/calls', content_type='application/json')
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_get_call(self):
        send_data = self.call1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/calls', send_data)
        del send_data['secret']
        send_data[u'id'] = 1
        resp = self.app.get('/calls/1')
        resp = OrderedDict((json.loads(resp.data)[0]))
        self.assertEqual(send_data, resp)

    def test_get_call__when_call_does_not_exist(self):
        resp = self.app.get('/calls/10000')
        self.assertEqual(0, len(json.loads(resp.data)))

    def test_put_call(self):
        send_data = self.call1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/calls', send_data)
        send_data[u'quality'] = 7
        send_data[u'id'] = 1
        resp = self.send_request(self.app.put, '/calls/1', send_data)
        del send_data['secret']
        self.assertEqual(send_data, json.loads(resp.data)[0])

    def test_put_call_when_call_does_not_exist(self):
        send_data = self.call1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/calls', send_data)
        del send_data['secret']
        resp = self.send_request(self.app.put, 'calls/10000', {'secret': self.token, 'name': 'name'})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_put_call_check_constraint(self):
        send_data = self.call1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/calls', send_data)
        resp = self.send_request(self.app.put, '/calls/1', {'secret': self.token, u'call_date': u'2012-12-21'})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_put_call_empty_data(self):
        send_data = self.call1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/calls', send_data)
        del send_data['secret']
        resp = self.send_request(self.app.put, 'calls/1', {'secret': self.token})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_put_call_not_null_constraint(self):
        send_data = self.call1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/calls', send_data)
        del send_data['secret']
        resp = self.send_request(self.app.put, '/calls/1', {'secret': self.token, u'name': None})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_put_call_unallowable_key(self):
        send_data = self.call1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/calls', send_data)
        del send_data['secret']
        resp = self.send_request(self.app.put, '/calls/1', {'secret': self.token, u'price': u'1231231'})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_delete_call(self):
        send_data = self.call1
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/calls', send_data)
        send_data = self.call2
        send_data['secret'] = self.token
        self.send_request(self.app.post, '/calls', send_data)
        self.app.delete('/calls/1/{}'.format(self.token))
        resp = self.app.get('/calls')
        self.assertEqual(len(json.loads(resp.data)), 1)
        self.app.delete('/calls/2/{}'.format(self.token))
        resp = self.app.get('/calls')
        self.assertEqual(len(json.loads(resp.data)), 0)

    def test_delete_call_when_call_does_not_exist(self):
        send_data = self.call1
        send_data['secret'] = self.token
        self.send_request(self.app.post, 'calls', send_data)
        self.app.delete('/calls/not_existing_call/{}'.format(self.token))
        resp = self.app.get('/calls')
        self.assertEqual(len(json.loads(resp.data)), 1)