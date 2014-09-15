"""
Test module for user account and ping
"""

import base64

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test.client import Client

from talon.models import Todo
from talon.tests.factories import UserFactory, TodoFactory


def create_test_user():
    """
    Create user for testing purposes
    """
    username = 'test'
    email = 'test@test.com'
    password = 'test'
    _ = User.objects.create_user(username, email, password)


class PingTest(TestCase):
    """
    Test pings
    """

    def test_ping(self):
        """
        Test if /ping call respond with pong
        """
        resp = self.client.get(reverse('ping'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'pong')


class AccountsTest(TestCase):
    """
    Test cases for managing user account
    """

    def test_user(self):
        """
        Create user with factory
        """
        self.assertEqual(User.objects.count(), 0)

        user = UserFactory()
        user.save()

        self.assertEqual(User.objects.count(), 1)


    def test_todo(self):
        """
        Create todo with factory
        """
        self.assertEqual(Todo.objects.count(), 0)

        user = UserFactory()
        user.save()
        todo = TodoFactory(user=user)
        todo.save()

        self.assertEqual(Todo.objects.count(), 1)


    def test_unicode(self):
        """
        Testing string representation of TOdo object
        """
        user = UserFactory()
        user.save()
        todo = TodoFactory(user=user, text=u'my task')
        todo.save()
        self.assertEqual(unicode(todo), u'my task')


    def test_can_login(self):
        """
        Create user and try to log in
        """
        create_test_user()
        login = self.client.login(username='test', password='test')
        self.assertEqual(login, True)



class APITest(TestCase):
    """
    Class for testing API calls
    """


    def setUp(self):
        self.client = Client()
        create_test_user()
        _ = self.client.login(username='test', password='test')


    def test_unauth_list(self):
        """
        Trying to get todo list without authentication
        """
        self.client = Client()
        resp = self.client.get('/api/todo/')
        self.assertEqual(resp.status_code, 401)
        pass


    def test_auth_list(self):
        """
        Trying to get todo list with session authentication
        """
        resp = self.client.get('/api/todo/')
        self.assertEqual(resp.status_code, 200)


    def test_basic_auth_list(self):
        """
        Trying to get todo list with session authentication
        """
        self.client = Client()
        self.client.defaults['HTTP_AUTHORIZATION'] = \
            'Basic ' + base64.b64encode('test:test')
        resp = self.client.get('/api/todo/')
        self.assertEqual(resp.status_code, 200)


    def test_unauth_create(self):
        """
        Create todo without authentication
        """
        self.client = Client()
        self.assertEqual(Todo.objects.count(), 0)

        resp = self.client.post('/api/todo/', {'text': 'asdf'})
        self.assertEqual(resp.status_code, 401)

        self.assertEqual(Todo.objects.count(), 0)


    def test_auth_create(self):
        """
        Create todo with session authentication
        """
        self.assertEqual(Todo.objects.count(), 0)

        resp = self.client.post('/api/todo/', {'text': 'asdf'})
        self.assertEqual(resp.status_code, 201)

        self.assertEqual(Todo.objects.count(), 1)


    def test_delete(self):
        """
        Test deletion of todo
        """
        self.test_auth_create()
        todo = Todo.objects.get()

        resp = self.client.delete('/api/todo/%s/' % (str(todo.id),))
        self.assertEqual(resp.status_code, 204)

        self.assertEqual(Todo.objects.count(), 0)


    def test_edit(self):
        """
        Changing text of todo
        """
        import json
        self.test_auth_create()
        todo = Todo.objects.get()
        self.assertEqual(todo.text, 'asdf')

        resp = self.client.put('/api/todo/%s/' % (str(todo.id),),
                               content_type='application/json',
                               data=json.dumps({'text': 'hello'}))

        self.assertEqual(resp.status_code, 200)
        todo = Todo.objects.get()
        self.assertEqual(todo.text, 'hello')

