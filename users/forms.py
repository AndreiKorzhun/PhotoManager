from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from users.models import User


class RegisterForm(UserCreationForm):
    """
    A form for creating a new user.
    """
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    """
    A form for logging a user in. Accepts username/password logins.
    """
    def confirm_login_allowed(self, user):
        """
        Allow all users to log in regardless of “active” status
        """
        pass
