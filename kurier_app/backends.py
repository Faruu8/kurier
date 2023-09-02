from django.contrib.auth.backends import ModelBackend

class CustomPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = self.model._default_manager.get(username=username)
        except self.model.DoesNotExist:
            return None

        if user.check_password(password) and user.is_courier and user.courier.phone == kwargs['phone']:
            return user
