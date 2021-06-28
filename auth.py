from rest_framework.authentication import SessionAuthentication


class CustomSessionAuthentication(SessionAuthentication):
    def authenticate_header(self, request):
        from django.conf import settings

        return 'Cookie form-action="{}", cookie-name="{}"'.format(
            settings.LOGIN_URL, settings.SESSION_COOKIE_NAME,
        )
