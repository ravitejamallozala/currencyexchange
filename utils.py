
from rest_framework.test import  APIClient
from django.contrib.sessions.middleware import SessionMiddleware
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from django.test import RequestFactory
from exchange_backend.models import User
from settings import UNITTEST_HTTP_HOST


def get_restframework_request(url, body, method="POST", args=None):
    req = RequestFactory(content_type="application/json")
    if method == "GET":
        req = req.get(url, content_type="application/json", data=body)
    else:
        req = req.post(url, content_type="application/json", data=body)

    req = Request(req)
    req.session = {}
    session_obj = SessionMiddleware()
    session_obj.process_request(req)
    return req


def get_authenticated_client():
    user = User.objects.filter(is_active=True).first()
    if getattr(user, "auth_token", None) is None:
        Token.objects.create(user=user)
    client = APIClient()
    client.credentials(HTTP_HOST=UNITTEST_HTTP_HOST)
    access_token = user.auth_token.key
    client.credentials(
        HTTP_AUTHORIZATION="Token " + access_token, HTTP_HOST=UNITTEST_HTTP_HOST,
    )
    return client, access_token
