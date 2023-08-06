from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Authentication backend which allows users to authenticate using either their
    email or username
    """

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(
                Q(email=username) | Q(username=username)
            )
            pwd_valid = user.check_password(password)
            if pwd_valid:
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
