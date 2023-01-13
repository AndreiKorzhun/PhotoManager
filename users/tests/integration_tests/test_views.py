from django.test import TestCase
from django.urls import reverse

from photoManager.settings import LOGIN_REDIRECT_URL, LOGIN_URL
from users.models import User


class UsersTestCase(TestCase):
    VIEW_PATH = 'users.views'
    test_password = '1234%^&*Qwer'

    def setUp(self):
        self.user = User.objects.create_user(username='test_username', password=self.test_password)

        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.register_url = reverse('register')

    def test_login__get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username', response.content)
        self.assertIn(b'Password', response.content)

    def test_login__form_is_valid(self):
        response = self.client.post(self.login_url, data={
            'username': 'test_username',
            'password': self.test_password,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(LOGIN_REDIRECT_URL))

    def test_login__form_is_invalid(self):
        response = self.client.post(self.login_url, data={
            'username': 'incorrect_test_username',
            'password': self.test_password,
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'Please enter a correct username and password. Note that both fields may be case-sensitive.',
            response.content,
        )

    def test_logout(self):
        self.client.login(username=self.user.username, password=self.test_password)
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(LOGIN_URL))

    def test_register__get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username', response.content)
        self.assertIn(b'Password', response.content)
        self.assertIn(b'Password confirmation', response.content)

    def test_register__form_is_valid(self):
        response = self.client.post(self.register_url, data={
            'username': 'test_username_2',
            'password1': self.test_password,
            'password2': self.test_password,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(LOGIN_REDIRECT_URL))

    def test_register__form_is_invalid(self):
        response = self.client.post(self.register_url, data={
            'username': 'test_username_2',
            'password1': self.test_password,
            'password2': "incorrect_password",
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'The two password fields didn\xe2\x80\x99t match.',
            response.content,
        )
