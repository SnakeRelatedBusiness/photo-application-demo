# accounts/tests/test_api.py
from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models import AppUser

class AuthAPITests(APITestCase):
    def setUp(self):
        self.username = 'user'
        self.password = 'password'
        self.user = AppUser.objects.create_user(username=self.username, password=self.password)

    def test_login_successful(self):
        payload = {
            'username': self.username,
            'password': self.password
        }

        response = self.client.post('/api/auth/login/', payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_bad_login_unauthorized(self):
        payload = {
            'username': self.username,
            'password': 'bad_password'
        }

        response = self.client.post('/api/auth/login/', payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_auth_status_endpoint(self):
        response_anon = self.client.get('/api/auth/me/')
        self.assertEqual(response_anon.status_code, status.HTTP_200_OK)
        self.assertFalse(response_anon.data['is_authenticated'])

        self.client.force_authenticate(user=self.user)
        response_auth = self.client.get('/api/auth/me/')

        self.assertEqual(response_auth.status_code, status.HTTP_200_OK)
        self.assertTrue(response_auth.data['is_authenticated'])
        self.assertEqual(response_auth.data['username'], self.username)