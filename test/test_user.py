from unittest.mock import patch
import json
import unittest
from server import server
from models.abc import db
from models import User
from repositories import UserRepository


class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = server.test_client()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_error(self):
        """ The GET on `/user` which is not in database
        should return an error """
        response = self.client.get('/api/users/Doe/John')

        self.assertEqual(response.status_code, 400)

    def test_get(self):
        """ The GET on `/user` should return an user """
        UserRepository.create(first_name='John', last_name='Doe', age=25)
        response = self.client.get('/api/users/Doe/John')

        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(
            response_json,
            {'user': {'age': 25, 'first_name': 'John', 'last_name': 'Doe'}}
        )

    def test_create_no_token(self):
        """ The POST on `/user` should not work if token is not valid """
        response = self.client.post(
            '/api/users/Doe/John',
            content_type='application/json',
            data=json.dumps({
                'age': 30
            })
        )

        self.assertEqual(response.status_code, 401)

    @patch('util.authorized.validate_token', return_value=False)
    def test_create_unauthorized(self, mock_decorator):
        """ The POST on `/user` should not work if token is not valid """
        response = self.client.post(
            '/api/users/Doe/John',
            content_type='application/json',
            headers={'Authorization': 'Bearer token'},
            data=json.dumps({
                'age': 30
            })
        )

        self.assertEqual(response.status_code, 401)

    @patch('util.authorized.validate_token', return_value=True)
    def test_create(self, mock_decorator):
        """ The POST on `/user` should create an user """
        UserRepository.create(first_name='John', last_name='Doe', age=25)
        response = self.client.post(
            '/api/users/Doe/John',
            content_type='application/json',
            headers={'Authorization': 'Bearer token'},
            data=json.dumps({
                'age': 30
            })
        )

        self.assertEqual(response.status_code, 400)

    @patch('util.authorized.validate_token', return_value=True)
    def test_create_duplicate(self, mock_decorator):
        """ The POST on `/user` should not create an user if already exists """
        response = self.client.post(
            '/api/users/Doe/John',
            content_type='application/json',
            headers={'Authorization': 'Bearer token'},
            data=json.dumps({
                'age': 30
            })
        )

        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(
            response_json,
            {'user': {'age': 30, 'first_name': 'John', 'last_name': 'Doe'}}
        )
        self.assertEqual(User.query.count(), 1)

    @patch('util.authorized.validate_token', return_value=True)
    def test_update(self, mock_decorator):
        """ The PUT on `/user` should update an user's age """
        UserRepository.create(first_name='John', last_name='Doe', age=25)
        response = self.client.put(
            '/api/users/Doe/John',
            content_type='application/json',
            headers={'Authorization': 'Bearer token'},
            data=json.dumps({
                'age': 30
            })
        )

        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(
            response_json,
            {'user': {'age': 30, 'first_name': 'John', 'last_name': 'Doe'}}
        )
        user = UserRepository.get(first_name='John', last_name='Doe')
        self.assertEqual(user.age, 30)
