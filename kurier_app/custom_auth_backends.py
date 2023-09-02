from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and user.is_courier and user.courier.phone == kwargs.get('phone'):
            return user
        return None
