import json

from rest_framework.test import force_authenticate, APIClient
from django.conf import settings
from importlib import import_module
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
import rest_framework.status
from exchange_backend.utils_tests import CommonTestCasesMixin
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory, APITestCase
from django.core.urlresolvers import reverse, resolve

from exchange_backend import views
from exchange_backend.models import User, Currency, Wallet, Transaction
from exchange_backend.views import WithdrawmoneyView, ProfileView, CurrencyViewset
from settings import UNITTEST_HTTP_HOST
from utils import get_restframework_request, get_authenticated_client


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
        self.assertEqual(resp.status_code, rest_framework.status.HTTP_200_OK)

    def test_registeruser(self):
        req = self.req.post(self.url, content_type="application/json", data=self.body)
        resp = views.RegisterView.as_view()(req)
        self.assertEqual(resp.status_code, rest_framework.status.HTTP_302_FOUND,
                         "As after registration it will redirect to Home page")
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
        body = {
            "username": "wronguser",
            "wrongkey": "test@123",
        }
        self.wronguser_body2 = json.dumps(body)

    def test_loginview(self):
        req = RequestFactory().get('login/')
        resp = views.LoginView.as_view()(req)
        assert resp.status_code == rest_framework.status.HTTP_200_OK

    def test_register_loginuser(self):
        req = self.regreq.post(self.registerurl, content_type="application/json", data=self.regbody)
        resp = views.RegisterView.as_view()(req)
        self.assertEqual(resp.status_code, rest_framework.status.HTTP_302_FOUND,
                         "As after registration it will redirect to Home page")
        self.assertTrue('' in resp.url)
        self.assertTrue(User.objects.filter(username="test").first() is not None, "As user is Sucessfully created")

        req = get_restframework_request("login/", self.body)
        resp = views.LoginView.as_view()(req)

        self.assertEqual(resp.status_code, rest_framework.status.HTTP_302_FOUND)
        self.assertTrue('/' in resp.url)
        self.assertTrue(User.objects.filter(username="test").first() is not None, "As user is Sucessfully created")

        req = get_restframework_request("login/", self.wronguser_body)
        resp = views.LoginView.as_view()(req)
        self.assertEqual(resp.status_code, 401, "Unauthorized Status code")

        req = get_restframework_request("login/", self.wronguser_body2)
        resp = views.LoginView.as_view()(req)
        self.assertEqual(resp.status_code, 401, "Unauthorized Status code")


class TestHomePage(TestCase):
    def setUp(self) -> None:
        self.req = RequestFactory().get('/')
        self.req.user = AnonymousUser()

    def test_homeview(self):
        resp = views.ServeFrontend.as_view()(self.req)
        self.assertEqual(resp.status_code, rest_framework.status.HTTP_200_OK)


class TestTransferPage(TestCase):
    def setUp(self) -> None:
        self.req = RequestFactory().get('transfer_view/')
        self.user = mixer.blend('exchange_backend.user')
        self.req.user = self.user

    def test_transferview(self):
        resp = views.TransferView.as_view()(self.req)
        self.assertEqual(resp.status_code, rest_framework.status.HTTP_200_OK)

    def test_transferviewAnonymus(self):
        self.req.user = AnonymousUser()
        resp = views.TransferView.as_view()(self.req)
        self.assertEqual(resp.status_code, rest_framework.status.HTTP_302_FOUND)
        self.assertTrue('/login' in resp.url)


class TestAddMoneyPage(TestCase):
    def setUp(self) -> None:
        self.req = RequestFactory().get('addmoney/')
        self.user = mixer.blend('exchange_backend.user')
        self.req.user = self.user

    def test_addmoneyview(self):
        resp = views.AddmoneyView.as_view()(self.req)
        self.assertEqual(resp.status_code, rest_framework.status.HTTP_200_OK)

    def test_addmoneyviewAnonymus(self):
        self.req.user = AnonymousUser()
        resp = views.AddmoneyView.as_view()(self.req)
        self.assertEqual(resp.status_code, rest_framework.status.HTTP_302_FOUND)
        self.assertTrue('/login' in resp.url)


class TestWithdrawPage(TestCase):

    def setUp(self) -> None:
        self.req = RequestFactory().get('withdraw/')
        self.user = mixer.blend('exchange_backend.user')
        self.req.user = self.user

    def test_withdrawview(self):
        resp = WithdrawmoneyView.as_view()(self.req)
        self.assertEqual(resp.status_code, rest_framework.status.HTTP_200_OK)

    def test_withdrawAnonymus(self):
        self.req.user = AnonymousUser()
        resp = views.WithdrawmoneyView.as_view()(self.req)
        self.assertEqual(resp.status_code, rest_framework.status.HTTP_302_FOUND)
        self.assertTrue('/login' in resp.url)


class TestProfilePage(TestCase):
    def setUp(self) -> None:
        self.req = RequestFactory().get('profile/')
        self.user = mixer.blend('exchange_backend.user')
        self.req.user = self.user

    def test_profileview(self):
        resp = ProfileView.as_view()(self.req)
        self.assertEqual(resp.status_code, rest_framework.status.HTTP_200_OK)

    def test_profileAnonymus(self):
        self.req.user = AnonymousUser()
        resp = views.ProfileView.as_view()(self.req)
        self.assertEqual(resp.status_code, rest_framework.status.HTTP_302_FOUND)
        self.assertTrue('/login' in resp.url)


class TestLogoutView(TestCase):
    def setUp(self) -> None:
        self.req = get_restframework_request("logout/", {}, "GET")
        self.user = mixer.blend('exchange_backend.user')
        self.req.user = self.user

    def test_logoutuser(self):
        resp = views.LogoutView.as_view()(self.req)
        self.assertEqual(resp.status_code, rest_framework.status.HTTP_302_FOUND,
                         "As after Logout it will redirect to Home page")
        self.assertTrue("/" is resp.url)


class TestCurrencyViewset(APITestCase, CommonTestCasesMixin):
    def setUp(self) -> None:
        self.url = reverse("currency-list")
        self.user = mixer.blend('exchange_backend.user')
        self.name = "currency"
        self.params = {}
        self.data = {"name": "TESTCURR"}
        self.invalid_data = {"name": None}
        self.invalid_data_fields = ("name",)
        self.client, self.access_token = get_authenticated_client()
        self.populate_url = reverse("currency-populate-currencies")

    def test_currency_get(self):
        self.client, self.access_token = get_authenticated_client()
        response = self.client.get(self.url)
        curr_count = Currency.objects.count()

        self.assertEqual(response.status_code, rest_framework.status.HTTP_200_OK)
        self.assertEqual(response.data['count'], curr_count)

    def test_populate_currencies_get(self):
        Currency.objects.all().delete()
        self.client, self.access_token = get_authenticated_client()
        response = self.client.get(self.populate_url)
        self.assertEqual(response.status_code, rest_framework.status.HTTP_200_OK)
        self.assertGreater(Currency.objects.count(), 100)


class TestUserViewset(APITestCase):
    def setUp(self) -> None:
        self.curr_obj = User.objects.first()
        self.url = reverse("user-list")
        self.user = mixer.blend('exchange_backend.user')
        self.wallet = mixer.blend('exchange_backend.wallet')
        self.curr = mixer.blend('exchange_backend.currency')
        self.name = "user"
        self.params = {}
        self.data = {
            "username": "test",
            "password": "test@123",
            "password2": "test@123",
            "email": "test@example.com",
            "first_name": "test",
            "last_name": "user",
            "groups": [],
            "wallet_id": self.wallet.id,
            "currency_id": self.curr.id
        }
        self.invalid_data = {
            "username": None,
            "password": "test@123",
            "password2": "test@123",
            "email": "test@example.com",
            "first_name": None,
            "last_name": 100,
            "groups": [],
            "wallet_id": self.wallet.id,
            "currency_id": self.curr.id
        }
        self.invalid_data_fields = ('username',
                                    'currency_id',
                                    'password2',
                                    'last_name',
                                    'groups',
                                    'first_name',
                                    'wallet_id',
                                    'password',
                                    'email')
        self.client, self.access_token = get_authenticated_client()
        self.currentuser_url = reverse("user-currentuser")

    def test_user_get(self):
        self.client, self.access_token = get_authenticated_client()
        response = self.client.get(self.url)
        user_count = User.objects.count()

        self.assertEqual(response.status_code, rest_framework.status.HTTP_200_OK)
        self.assertEqual(response.data['count'], user_count)

    def test_get_currentuser(self):
        self.client, self.access_token = get_authenticated_client()
        response = self.client.get(self.currentuser_url)
        self.assertEqual(response.status_code, rest_framework.status.HTTP_200_OK)
        self.assertEqual(response.data["id"], User.objects.first().id)


class TestWalletViewset(APITestCase, CommonTestCasesMixin):
    def setUp(self) -> None:
        self.url = reverse("wallet-list")
        self.user = mixer.blend('exchange_backend.user')
        self.curr = mixer.blend('exchange_backend.currency')
        self.name = "wallet"
        self.params = {}
        self.data = {"current_balance": 100, "currency_type": self.curr.id}
        self.invalid_data = {"current_balance": "ravi", "currency_type": self.curr.id}
        self.invalid_data_fields = ("current_balance" "currency_type")
        self.client, self.access_token = get_authenticated_client()

    def test_wallet_get(self):
        self.client, self.access_token = get_authenticated_client()
        response = self.client.get(self.url)
        wall_count = Wallet.objects.count()

        self.assertEqual(response.status_code, rest_framework.status.HTTP_200_OK)
        self.assertEqual(response.data['count'], wall_count)


class TestTransactionViewset(APITestCase, CommonTestCasesMixin):
    def setUp(self) -> None:
        self.url = reverse("transaction-list")
        self.wallet_transaction_url = reverse("transaction-wallet-transaction")
        self.transfer_money_url = reverse("transaction-transfer-money")
        self.wallet_obj = mixer.blend('exchange_backend.Wallet', current_balance=2000)
        self.curr_obj = mixer.blend('exchange_backend.Currency', name="INR")
        self.new_curr_obj = mixer.blend('exchange_backend.Currency')
        self.user_obj = mixer.blend('exchange_backend.User', username="testuser", first_name="test",
                                    wallet=self.wallet_obj,
                                    default_currency=self.curr_obj)

        self.name = "transaction"
        self.params = {}
        self.data = {
            "user": self.user_obj.id,
            "dest_user_id": None,
            "transaction_type": "debit",
            "amount": 100,
            "currency_type": self.curr_obj.id,
            "remaining_balance": 0,
            "status": "accepted",
            "description": "Test Description",
        }
        self.invalid_data = {
            "user": self.user_obj.id,
            "dest_user_id": None,
            "transaction_type": "debits",
            "amount": "100",
            "currency_type": self.curr_obj.id,
            "remaining_balance": 0,
            "status": "accepteds",
            "description": "Test Description",
        }
        self.invalid_data_fields = (
            "user"
            "dest_user_id",
            "transaction_type",
            "amount",
            "currency_type",
            "remaining_balance",
            "status",
            "description"
        )
        self.client, self.access_token = get_authenticated_client()

    def test_wallet_get(self):
        self.client, self.access_token = get_authenticated_client()
        response = self.client.get(self.url)
        trasn_count = Transaction.objects.count()

        self.assertEqual(response.status_code, rest_framework.status.HTTP_200_OK)
        self.assertEqual(response.data['count'], trasn_count)

    def test_wallet_transaction_add_moeny(self):
        self.client, self.access_token = get_authenticated_client()
        old_balance = self.user_obj.wallet.current_balance
        money = 100
        data = {
            "amount": money,
            "currency_id": self.curr_obj.id,
            "to_user_id": self.user_obj.id,
            "transaction_type": "credit",
        }
        response = self.client.post(self.wallet_transaction_url, data=data)
        user = User.objects.filter(username="testuser").first()
        self.assertEqual(response.status_code, rest_framework.status.HTTP_200_OK)
        self.assertEqual(user.wallet.current_balance, old_balance + money)

    def test_wallet_transaction_withdraw_money(self):
        self.client, self.access_token = get_authenticated_client()
        old_balance = self.user_obj.wallet.current_balance
        money = 5000
        data = {
            "amount": money,
            "currency_id": self.curr_obj.id,
            "transaction_type": "debit",
        }
        response = self.client.post(self.wallet_transaction_url, data=data)
        self.assertEqual(response.status_code, rest_framework.status.HTTP_400_BAD_REQUEST,
                         "Amount cannot be Withdrawn as Balance is lesser than withdrawing amount")
        self.assertEqual(response.data[0], "Amount cannot be Withdrawn as Balance is lesser than withdrawing amount ")

    def test_wallet_transaction_withdraw_money_correct(self):
        self.client, self.access_token = get_authenticated_client()
        self.wallet_obj2 = mixer.blend('exchange_backend.Wallet', current_balance=2000)

        user_obj2 = mixer.blend('exchange_backend.User', username="testuser2", first_name="test",
                                wallet=self.wallet_obj2,
                                default_currency=self.curr_obj)
        old_balance = user_obj2.wallet.current_balance
        money = 100
        data = {
            "amount": money,
            "currency_id": self.curr_obj.id,
            "transaction_type": "debit",
        }
        response = self.client.post(self.wallet_transaction_url, data=data)
        user = User.objects.filter(username="testuser").first()
        self.assertEqual(response.status_code, rest_framework.status.HTTP_200_OK,
                         "Amount can be Withdrawn as Balance is Greater than withdrawing amount")
        self.assertEqual(user.wallet.current_balance, old_balance - money)

    def test_wallet_transaction_transfer_money(self):
        self.client, self.access_token = get_authenticated_client()
        self.wallet_obj2 = mixer.blend('exchange_backend.Wallet', current_balance=2000)
        user_obj2 = mixer.blend('exchange_backend.User', username="testuser2", first_name="test",
                                wallet=self.wallet_obj2,
                                default_currency=self.curr_obj)
        money = 100
        data = {
            "amount": money,
            "currency_id": self.curr_obj.id,
            "to_user_id": user_obj2.id,
        }
        user_2_balance = user_obj2.wallet.current_balance
        user_1_balance = self.user_obj.wallet.current_balance
        response = self.client.post(self.transfer_money_url, data=data)
        user = User.objects.filter(username="testuser").first()
        user2 = User.objects.filter(username="testuser2").first()
        self.assertEqual(response.status_code, rest_framework.status.HTTP_200_OK,
                         "Amount can be Transfered as Balance is Greater than transfering amount")
        self.assertEqual(user.wallet.current_balance, user_1_balance - money)
        self.assertEqual(user2.wallet.current_balance, user_2_balance + money)

    def test_wallet_transaction_transfer_money_fail(self):
        self.client, self.access_token = get_authenticated_client()
        self.wallet_obj2 = mixer.blend('exchange_backend.Wallet', current_balance=2000)
        user_obj2 = mixer.blend('exchange_backend.User', username="testuser2", first_name="test",
                                wallet=self.wallet_obj2,
                                default_currency=self.curr_obj)
        money = 10000
        data = {
            "amount": money,
            "currency_id": self.curr_obj.id,
            "to_user_id": user_obj2.id,
        }
        user_2_balance = user_obj2.wallet.current_balance
        user_1_balance = self.user_obj.wallet.current_balance
        response = self.client.post(self.transfer_money_url, data=data)
        user = User.objects.filter(username="testuser").first()
        user2 = User.objects.filter(username="testuser2").first()
        self.assertEqual(response.status_code, rest_framework.status.HTTP_400_BAD_REQUEST,
                         "Amount cannot be Transfered as Balance is lesser than transfering amount")
        self.assertEqual(user.wallet.current_balance, user_1_balance)
        self.assertEqual(user2.wallet.current_balance, user_2_balance)
