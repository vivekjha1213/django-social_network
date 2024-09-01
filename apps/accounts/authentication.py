# apps/accounts/authentication.py

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        email = kwargs.get("email", username)
        print(f"emai and pass: {email} and {password}")
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except Exception as e:
            print(e)
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
