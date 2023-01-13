from unittest.mock import patch, MagicMock

from django.test import SimpleTestCase

from photoManager.settings import LOGIN_REDIRECT_URL, LOGIN_URL
from users.views import login_view, logout_view, register


class UsersViewsTestCase(SimpleTestCase):
    VIEW_PATH = 'users.views'

    @patch(f'{VIEW_PATH}.render')
    @patch(f'{VIEW_PATH}.LoginForm')
    def test_login_view__get(self, form_patch, render_patch):
        request_mock = MagicMock(method="GET")

        result = login_view(request_mock)

        self.assertEqual(result, render_patch.return_value)
        render_patch.assert_called_once_with(request_mock, "users/login.html", {
            "form": form_patch.return_value
        })
        form_patch.assert_called_once_with()

    @patch(f'{VIEW_PATH}.reverse')
    @patch(f'{VIEW_PATH}.HttpResponseRedirect')
    @patch(f'{VIEW_PATH}.login')
    @patch(f'{VIEW_PATH}.LoginForm')
    def test_login_view__form_is_valid(self, form_patch, login_patch, http_redirect_patch, reverse_patch):
        request_mock = MagicMock(method="POST")

        form_mock = MagicMock()
        form_mock.is_valid.return_value = True
        form_patch.return_value = form_mock

        reverse_mock = MagicMock()
        reverse_patch.return_value = reverse_mock

        result = login_view(request_mock)

        self.assertEqual(result, http_redirect_patch.return_value)
        form_patch.assert_called_once_with(data=request_mock.POST)
        form_mock.is_valid.assert_called_once_with()
        login_patch.assert_called_once_with(request_mock, form_mock.get_user.return_value)
        reverse_patch.assert_called_once_with(LOGIN_REDIRECT_URL)
        http_redirect_patch.assert_called_once_with(reverse_mock)

    @patch(f'{VIEW_PATH}.render')
    @patch(f'{VIEW_PATH}.LoginForm')
    def test_login_view__form_is_invalid(self, form_patch, render_patch):
        request_mock = MagicMock(method="POST")

        form_mock = MagicMock()
        form_mock.is_valid.return_value = False
        form_patch.return_value = form_mock

        result = login_view(request_mock)

        self.assertEqual(result, render_patch.return_value)
        form_patch.assert_called_once_with(data=request_mock.POST)
        form_mock.is_valid.assert_called_once_with()
        render_patch.assert_called_once_with(request_mock, "users/login.html", {
            "form": form_mock
        })

    @patch(f'{VIEW_PATH}.HttpResponseRedirect')
    @patch(f'{VIEW_PATH}.reverse')
    @patch(f'{VIEW_PATH}.logout')
    def test_logout_view(self, logout_patch, reverse_patch, http_redirect_patch):
        request_mock = MagicMock()

        reverse_mock = MagicMock()
        reverse_patch.return_value = reverse_mock

        result = logout_view(request_mock)

        self.assertEqual(result, http_redirect_patch.return_value)
        logout_patch.assert_called_once_with(request_mock)
        reverse_patch.assert_called_once_with(LOGIN_URL)
        http_redirect_patch.assert_called_once_with(reverse_mock)

    @patch(f'{VIEW_PATH}.render')
    @patch(f'{VIEW_PATH}.RegisterForm')
    def test_register__get(self, form_patch, render_patch):
        request_mock = MagicMock(method="GET")

        result = register(request_mock)

        self.assertEqual(result, render_patch.return_value)
        render_patch.assert_called_once_with(request_mock, "users/register.html", {
            "form": form_patch.return_value
        })
        form_patch.assert_called_once_with()

    @patch(f'{VIEW_PATH}.reverse')
    @patch(f'{VIEW_PATH}.HttpResponseRedirect')
    @patch(f'{VIEW_PATH}.login')
    @patch(f'{VIEW_PATH}.RegisterForm')
    def test_register__form_is_valid(self, form_patch, login_patch, http_redirect_patch, reverse_patch):
        request_mock = MagicMock(method="POST")

        form_mock = MagicMock()
        form_mock.is_valid.return_value = True
        form_patch.return_value = form_mock
        user_mock = MagicMock()
        form_mock.save.return_value = user_mock

        reverse_mock = MagicMock()
        reverse_patch.return_value = reverse_mock

        result = register(request_mock)

        self.assertEqual(result, http_redirect_patch.return_value)
        form_patch.assert_called_once_with(request_mock.POST)
        form_mock.is_valid.assert_called_once_with()
        login_patch.assert_called_once_with(request_mock, user_mock)
        reverse_patch.assert_called_once_with(LOGIN_REDIRECT_URL)
        http_redirect_patch.assert_called_once_with(reverse_mock)

    @patch(f'{VIEW_PATH}.render')
    @patch(f'{VIEW_PATH}.RegisterForm')
    def test_register__form_is_invalid(self, form_patch, render_patch):
        request_mock = MagicMock(method="POST")

        form_mock = MagicMock()
        form_mock.is_valid.return_value = False
        form_patch.return_value = form_mock

        result = register(request_mock)

        self.assertEqual(result, render_patch.return_value)
        form_patch.assert_called_once_with(request_mock.POST)
        form_mock.is_valid.assert_called_once_with()
        render_patch.assert_called_once_with(request_mock, "users/register.html", {
            "form": form_mock
        })
