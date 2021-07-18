import json

import pytest
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from exchange_backend import views
from mixer.backend.django import mixer
from rest_framework.request import Request
from exchange_backend.views import WithdrawmoneyView, ProfileView, User
from utils import get_restframework_request

pytestmark = pytest.mark.django_db


class TestRegisterPage:
    def test_registerview(self):
        req = RequestFactory().get('register/')
        resp = views.RegisterView.as_view()(req)
        assert resp.status_code == 200

    def test_registeruser(self):
        body = {
            "username": "test",
            "password": "test@123",
            "password2": "test@123",
            "email": "test@example.com",
            "first_name": "test",
            "last_name": "user"
        }
        body = json.dumps(body)
        req = RequestFactory(content_type="application/json")
        req = req.post('register/', content_type="application/json", data=body)
        resp = views.RegisterView.as_view()(req)
        assert resp.status_code == 302, "As after registration it will redirect to Home page"
        assert '' in resp.url
        assert User.objects.filter(username="test").first() is not None, "As user is Sucessfully created"


class TestLoginPage:
    def test_loginview(self):
        req = RequestFactory().get('login/')
        resp = views.LoginView.as_view()(req)
        assert resp.status_code == 200

    def test_register_loginuser(self):
        body = {
            "username": "test",
            "password": "test@123",
            "password2": "test@123",
            "email": "test@example.com",
            "first_name": "test",
            "last_name": "user"
        }
        body = json.dumps(body)
        req = RequestFactory(content_type="application/json")
        req = req.post('register/', content_type="application/json", data=body)
        resp = views.RegisterView.as_view()(req)
        assert resp.status_code == 302, "As after registration it will redirect to Home page"
        assert '' in resp.url
        assert User.objects.filter(username="test").first() is not None, "As user is Sucessfully created"
        body = {
            "username": "test",
            "password": "test@123",
        }
        body = json.dumps(body)
        req = get_restframework_request("login/", body)
        resp = views.LoginView.as_view()(req)
        assert resp.status_code == 302, "As after Success Login it will redirect to Home page"
        assert resp.url == '/', "As after Successful Login it will redirect to Home page"
        body = {
            "username": "wronguser",
            "password": "test@123",
        }
        body = json.dumps(body)
        req = get_restframework_request("login/", body)
        resp = views.LoginView.as_view()(req)
        assert resp.status_code == 401, "unauthorized Status code"
        body = {
            "username": "test",
            "password": "test@123",
        }
        body = json.dumps(body)
        req = get_restframework_request("login/", body)
        resp = views.LoginView.as_view()(req)
        assert resp.status_code == 302, "Redirect Status code"
        assert resp.url == '/', "As after Successful Login it will redirect to Home page"


class TestLogoutView:
    def test_logoutuser(self):
        user = mixer.blend('exchange_backend.user')
        req = get_restframework_request("logout/", {})
        req.user = user
        resp = views.LogoutView.as_view()(req)
        assert resp.status_code == 302, "As after Logout it will redirect to Home page"
        assert '' in resp.url


class TestHomePage:
    def test_homeview(self):
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = views.ServeFrontend.as_view()(req)
        assert resp.status_code == 200


class TestTransferPage:
    def test_transferview(self):
        req = RequestFactory().get('transfer_view/')
        user = mixer.blend('exchange_backend.user')
        req.user = user
        resp = views.TransferView.as_view()(req)
        assert resp.status_code == 200

    def test_transferviewAnonymus(self):
        req = RequestFactory().get('transfer_view/')
        req.user = AnonymousUser()
        resp = views.TransferView.as_view()(req)
        assert resp.status_code == 302
        assert 'login' in resp.url


class TestAddMoneyPage:
    def test_addmoneyview(self):
        req = RequestFactory().get('addmoney/')
        user = mixer.blend('exchange_backend.user')
        req.user = user
        resp = views.AddmoneyView.as_view()(req)
        assert resp.status_code == 200

    def test_addmoneyviewAnonymus(self):
        req = RequestFactory().get('addmoney/')
        req.user = AnonymousUser()
        resp = views.AddmoneyView.as_view()(req)
        assert resp.status_code == 302
        assert 'login' in resp.url


class TestWithdrawPage:
    def test_withdrawview(self):
        req = RequestFactory().get('withdraw/')
        user = mixer.blend('exchange_backend.user')
        req.user = user
        resp = WithdrawmoneyView.as_view()(req)
        assert resp.status_code == 200

    def test_withdrawAnonymus(self):
        req = RequestFactory().get('withdraw/')
        req.user = AnonymousUser()
        resp = views.WithdrawmoneyView.as_view()(req)
        assert resp.status_code == 302
        assert 'login' in resp.url


class TestProfilePage:
    def test_profileview(self):
        req = RequestFactory().get('profile/')
        user = mixer.blend('exchange_backend.user')
        req.user = user
        resp = ProfileView.as_view()(req)
        assert resp.status_code == 200

    def test_profileAnonymus(self):
        req = RequestFactory().get('profile/')
        req.user = AnonymousUser()
        resp = views.ProfileView.as_view()(req)
        assert resp.status_code == 302
        assert 'login' in resp.url
