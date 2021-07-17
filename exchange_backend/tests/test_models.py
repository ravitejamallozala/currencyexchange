import pytest
from mixer.backend.django import mixer
from django.core.exceptions import ValidationError
from exchange_backend.models import User

pytestmark = pytest.mark.django_db


class TestCurrency:
    def test_create(self):
        obj = mixer.blend('exchange_backend.Currency')
        assert obj.pk == 1, 'Checking the added record in DB'

    def test_print(self):
        obj = mixer.blend('exchange_backend.Currency', name="INR")
        assert obj.__str__() == "INR", 'Checking the added record in DB'

    def test_create_name(self):
        obj = mixer.blend('exchange_backend.Currency', name="INR")
        assert obj.name == "INR", 'Checking the added record in DB has given value in name column'

    def test_create_none(self):
        try:
            obj = mixer.blend('exchange_backend.Currency', name=None)
        except ValidationError as e:
            assert True, 'Checking the added record in DB has given value in name column'
        else:
            assert False


class TestWallet:
    def test_create(self):
        obj = mixer.blend('exchange_backend.Wallet')
        assert obj.pk == 1, 'Checking the added record in DB'

    def test_create_data(self):
        curr_obj = mixer.blend('exchange_backend.Currency', name="INR")
        obj = mixer.blend('exchange_backend.Wallet', current_balance=100, currency_type=curr_obj)
        assert obj.current_balance == 100.0, 'Checking the added record in DB has given value in name column'
        assert obj.currency_type.id == curr_obj.pk, 'Checking the added record in DB has given foreign key relation'

    def test_create_none(self):
        try:
            obj = mixer.blend('exchange_backend.Wallet', current_balance=None)
        except ValidationError as e:
            assert True, 'Checking the added record in DB has given value in balance'
        else:
            assert False


class TestUser:
    def test_create(self):
        obj = mixer.blend('exchange_backend.User')
        assert obj.pk == 1, 'Checking the added record in DB'

    def test_create_data(self):
        wallet_obj = mixer.blend('exchange_backend.Wallet')
        curr_obj = mixer.blend('exchange_backend.Currency')
        user_obj = mixer.blend('exchange_backend.User', wallet=wallet_obj, default_currency=curr_obj)
        assert user_obj.default_currency.id == curr_obj.id, 'Checking the added record in DB has given foreign key relation'
        assert user_obj.wallet == wallet_obj, 'Checking the added record in DB has given value in Currency column'

    def test_create_none_currency(self):
        try:
            obj = mixer.blend('exchange_backend.User', default_currency=None)
        except ValidationError as e:
            assert False, 'Checking the added record in DB has given value in Currency'
        else:
            assert True

    def test_create_none_wallet(self):
        try:
            obj = mixer.blend('exchange_backend.User', Wallet=None)
        except ValidationError as e:
            assert False, 'Checking the added record in DB has given value in wallet'
        else:
            assert True

    def test_create_default_values(self):
        user_obj = mixer.blend('exchange_backend.User', wallet=None, default_currency=None)
        User.create_default_values(user_obj)
        assert user_obj.default_currency.name == "INR"
        User.create_default_values(user_obj)
        assert user_obj.default_currency.name == "INR"

    def test_user_postsave(self):
        curr_obj = mixer.blend('exchange_backend.Currency', name="INR")
        wallet_obj = mixer.blend('exchange_backend.Wallet')

        user_obj = User.objects.create(username="test", password="test@123", default_currency=curr_obj,
                                       wallet=wallet_obj)
        user_obj.username = "test2"
        user_obj.save()
        user_obj = User.objects.first()
        curr_obj = mixer.blend('exchange_backend.Currency', name="USD")
        user_obj.default_currency = curr_obj
        user_obj.save()

    def test_update_currency(self):
        wallet_obj = mixer.blend('exchange_backend.Wallet')
        curr_obj = mixer.blend('exchange_backend.Currency')
        user_obj = User.objects.create(username="test", password="test@123", wallet=wallet_obj)
        User.create_default_values(user_obj)
        user_obj.default_currency.name = "GBP"
        user_obj.save()
        assert user_obj.wallet.currency_type.name == "INR"


class TestTransaction:
    def test_create(self):
        curr_obj = mixer.blend('exchange_backend.Currency', name="INR")
        wallet_obj = mixer.blend('exchange_backend.Wallet')

        user_obj = User.objects.create(username="test", password="test@123", default_currency=curr_obj,
                                       wallet=wallet_obj)
        obj = mixer.blend('exchange_backend.Transaction', user=user_obj, currency_type=curr_obj)
        assert obj.pk == 1, 'Checking the added record in DB'

    def test_create_data(self):
        curr_obj = mixer.blend('exchange_backend.Currency')
        wallet_obj = mixer.blend('exchange_backend.Wallet')
        user_obj = mixer.blend('exchange_backend.User', wallet=wallet_obj)
        trans_obj = mixer.blend('exchange_backend.Transaction', transaction_type="debit", currency_type=curr_obj,
                                user=user_obj)
        assert trans_obj.transaction_type == "debit", 'Checking the added record in DB has given value in name column'
        assert trans_obj.user.id == user_obj.pk, 'Checking the added record in DB has given foreign key relation'

    def test_create_none(self):
        try:
            obj = mixer.blend('exchange_backend.Transaction', user=None)
        except ValidationError as e:
            assert True, 'Checking the added record in DB has given value in user'
        else:
            assert False
