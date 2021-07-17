import json
from django.conf import settings
from importlib import import_module

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory

from exchange_backend import views
from exchange_backend.models import User
from utils import get_restframework_request


class RegisterPageTest(TestCase):
    def setUp(self):
        body = {
            "username": "test",
            "password": "test@123",
            "password2": "test@123",
            "email": "test@example.com",
            "first_name": "test",
            "last_name": "user"
        }
        self.body = json.dumps(body)
        self.url = "register/"
        self.req = RequestFactory(content_type="application/json")

    def test_registerview(self):
        req = RequestFactory().get('register/')
        resp = views.RegisterView.as_view()(req)
        self.assertEqual(resp.status_code, 200)

    def test_registeruser(self):
        req = self.req.post(self.url, content_type="application/json", data=self.body)
        resp = views.RegisterView.as_view()(req)
        self.assertEqual(resp.status_code, 302, "As after registration it will redirect to Home page")
        self.assertTrue('' in resp.url)
        self.assertTrue(User.objects.filter(username="test").first() is not None, "As user is Sucessfully created")


class TestLoginPage(TestCase):
    def setUp(self):
        body = {
            "username": "test",
            "password": "test@123",
            "password2": "test@123",
            "email": "test@example.com",
            "first_name": "test",
            "last_name": "user"
        }
        self.regbody = json.dumps(body)
        self.registerurl = "register/"
        body = {
            "username": "test",
            "password": "test@123",
        }
        self.body = json.dumps(body)
        self.url = "login/"
        self.regreq = RequestFactory(content_type="application/json")
        body = {
            "username": "wronguser",
            "password": "test@123",
        }
        self.wronguser_body = json.dumps(body)

    def test_loginview(self):
        req = RequestFactory().get('login/')
        resp = views.LoginView.as_view()(req)
        assert resp.status_code == 200

    def test_register_loginuser(self):
        req = self.regreq.post(self.registerurl, content_type="application/json", data=self.regbody)
        resp = views.RegisterView.as_view()(req)
        self.assertEqual(resp.status_code, 302, "As after registration it will redirect to Home page")
        self.assertTrue('' in resp.url)
        self.assertTrue(User.objects.filter(username="test").first() is not None, "As user is Sucessfully created")

        req = get_restframework_request("login/", self.body)
        resp = views.LoginView.as_view()(req)

        self.assertEqual(resp.status_code, 302)
        self.assertTrue('/' in resp.url)
        self.assertTrue(User.objects.filter(username="test").first() is not None, "As user is Sucessfully created")

        req = get_restframework_request("login/", self.wronguser_body)
        resp = views.LoginView.as_view()(req)
        self.assertEqual(resp.status_code, 401, "Unauthorized Status code")


class TestHomePage(TestCase):
    def setUp(self) -> None:
        self.req = RequestFactory().get('/')
        self.req.user = AnonymousUser()

    def test_homeview(self):
        resp = views.ServeFrontend.as_view()(self.req)
        self.assertEqual(resp.status_code, 200)


class TestTransferPage(TestCase):
    def setUp(self) -> None:
        self.req = RequestFactory().get('transfer_view/')
        self.user = mixer.blend('exchange_backend.user')
        self.req.user = self.user

    def test_transferview(self):
        resp = views.TransferView.as_view()(self.req)
        self.assertEqual(resp.status_code, 200)

    def test_transferviewAnonymus(self):
        self.req.user = AnonymousUser()
        resp = views.TransferView.as_view()(self.req)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue('/login' in resp.url)


class TestAddMoneyPage(TestCase):

    def setUp(self) -> None:
        self.req = RequestFactory().get('addmoney/')
        self.user = mixer.blend('exchange_backend.user')
        self.req.user = self.user

    def test_addmoneyview(self):
        resp = views.AddmoneyView.as_view()(self.req)
        self.assertEqual(resp.status_code, 200)

    def test_addmoneyviewAnonymus(self):
        self.req.user = AnonymousUser()
        resp = views.AddmoneyView.as_view()(self.req)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue('/login' in resp.url)
