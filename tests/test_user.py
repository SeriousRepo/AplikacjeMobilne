import unittest
from collections import OrderedDict
from flask import json

from tests.tests import ApiTestCase


class UserTestCase(ApiTestCase):
    def setUp(self):
        super(self.__class__, self).setUp()
        self.user1 = {u'login': u'user1', u'password': u'pswd1',
                      u'phone_number': u'123454589', u'email': u'mail1@mail1.mail1',
                      u'birth_date': u'1111-11-11', u'name': u'John',
                      u'surname': u'Doe', u'sex': u'M'}

        self.user2 = {u'login': u'user2', u'password': u'pswd2',
                      u'phone_number': u'987654321', u'email': u'mail2@mail2.mail2',
                      u'birth_date': u'1111-11-11', u'name': u'Jane',
                      u'surname': u'Doe', u'sex': u'W'}

    def test_empty_db(self):
        resp = self.app.get('/users')
        self.assertEqual(0, len(json.loads(resp.data)))

    def test_get_users(self):
        resp = self.app.get('/users')
        self.assertEqual(0, len(json.loads(resp.data)))

        self.send_request(self.app.post, '/users', self.user1)

        resp = self.app.get('/users')
        self.assertEqual(1, len(json.loads(resp.data)))

        self.send_request(self.app.post, '/users', self.user2)

        resp = self.app.get('/users')
        self.assertEqual(2, len(json.loads(resp.data)))

    def test_post_user(self):
        send_data = self.choose_keys(self.user1, (u'login', u'password', u'phone_number', u'email'))
        resp = self.send_request(self.app.post, '/users', send_data)
        send_data.update({u'birth_date': None, u'name': None, u'surname': None, u'sex': None, u'id': 1})
        self.assertEqual(send_data, json.loads(resp.data)[0])
        send_data = self.user2
        resp = self.send_request(self.app.post, '/users', send_data)
        send_data[u'id'] = 2
        self.assertEqual(send_data, json.loads(resp.data)[0])

    def test_post_user_not_unique_constraint(self):
        send_data = self.choose_keys(self.user1, (u'login', u'password', u'phone_number', u'email'))
        self.send_request(self.app.post, '/users', send_data)
        send_data = self.user2
        send_data[u'login'] = self.user1[u'login']
        resp = self.send_request(self.app.post, '/users', send_data)
        self.assertEqual("400 BAD REQUEST", resp.status)

    def test_post_user_not_null_constraint(self):
        send_data = self.user1
        del send_data[u'phone_number']
        resp = self.send_request(self.app.post, '/users', send_data)
        self.assertEqual("400 BAD REQUEST", resp.status)

    def test_post_user_unallowable_(self):
        send_data = self.user1
        send_data[u'price'] = 1500
        resp = self.send_request(self.app.post, '/users', send_data)
        self.assertEqual("400 BAD REQUEST", resp.status)

    def test_post_user_check_constraint(self):
        send_data = self.user1
        send_data[u'sex'] = u'K'
        resp = self.send_request(self.app.post, '/users', send_data)
        self.assertEqual('400 BAD REQUEST', resp.status)

        send_data = self.user1
        send_data[u'phone_number'] = u'11111'
        resp = self.send_request(self.app.post, '/users', send_data)
        self.assertEqual('400 BAD REQUEST', resp.status)

        send_data = self.user1
        send_data[u'email'] = u'email'
        resp = self.send_request(self.app.post, '/users', send_data)
        self.assertEqual('400 BAD REQUEST', resp.status)

        send_data = self.user1
        send_data[u'birth_date'] = u'131321321'
        resp = self.send_request(self.app.post, '/users', send_data)
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_post_user_empty_data(self):
        resp = self.app.post('/users', content_type='application/json')
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_get_user(self):
        send_data = self.user1
        self.send_request(self.app.post, '/users', send_data)
        send_data[u'id'] = 1
        resp = self.app.get('/users/user1')
        resp = OrderedDict((json.loads(resp.data)[0]))
        self.assertEqual(send_data, resp)

    def test_get_user__when_user_does_not_exist(self):
        resp = self.app.get('/users/not_existing_user')
        self.assertEqual(0, len(json.loads(resp.data)))

    def test_put_user(self):
        send_data = self.user1
        self.send_request(self.app.post, '/users', send_data)
        send_data[u'password'] = u'pswd'
        send_data[u'id'] = 1
        resp = self.send_request(self.app.put, '/users/user1', send_data)
        self.assertEqual(send_data, json.loads(resp.data)[0])

    def test_put_user_when_user_does_not_exist(self):
        send_data = self.user1
        self.send_request(self.app.post, '/users', send_data)
        resp = self.send_request(self.app.put, 'users/not_existing_user', {u'password': u'pswd'})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_put_user_empty_data(self):
        send_data = self.user1
        self.send_request(self.app.post, '/users', send_data)
        resp = self.send_request(self.app.put, 'users/user1', {})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_put_user_unique_constraint(self):
        send_data = self.user1
        self.send_request(self.app.post, '/users', send_data)
        send_data = self.user2
        self.send_request(self.app.post, '/users', send_data)
        resp = self.send_request(self.app.put, 'users/user2', {u'login': u'user1'})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_put_user_not_null_constraint(self):
        send_data = self.user1
        self.send_request(self.app.post, '/users', send_data)
        resp = self.send_request(self.app.put, '/users/user1', {u'login': None})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_put_user_check_constraint(self):
        send_data = self.user1
        self.send_request(self.app.post, '/users', send_data)
        resp = self.send_request(self.app.put, '/users/user1', {u'sex': u'K'})
        self.assertEqual('400 BAD REQUEST', resp.status)

        resp = self.send_request(self.app.put, '/users/user1', {u'phone_number': u'11111'})
        self.assertEqual('400 BAD REQUEST', resp.status)

        resp = self.send_request(self.app.put, '/users/user1', {u'email': u'email'})
        self.assertEqual('400 BAD REQUEST', resp.status)

        resp = self.send_request(self.app.put, '/users/user1', {u'birth_date': u'3212312313'})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_put_user_unallowable_key(self):
        send_data = self.user1
        self.send_request(self.app.post, '/users', send_data)
        resp = self.send_request(self.app.put, '/users/user1', {u'price': u'1231231'})
        self.assertEqual('400 BAD REQUEST', resp.status)

    def test_delete_user(self):
        self.send_request(self.app.post, '/users', self.user1)
        self.send_request(self.app.post, '/users', self.user2)
        self.app.delete('/users/user1')
        resp = self.app.get('/users')
        self.assertEqual(len(json.loads(resp.data)), 1)
        self.app.delete('/users/user2')
        resp = self.app.get('/users')
        self.assertEqual(len(json.loads(resp.data)), 0)

    def test_delete_user_when_user_does_not_exist(self):
        self.send_request(self.app.post, 'users', self.user1)
        self.app.delete('/users/not_existing_user')
        resp = self.app.get('/users')
        self.assertEqual(len(json.loads(resp.data)), 1)