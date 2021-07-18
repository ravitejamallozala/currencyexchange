from django.test import TestCase
from mixer.backend.django import mixer
from django.core.exceptions import ValidationError
from exchange_backend.models import User, Currency, Wallet, Transaction


class TestCurrency(TestCase):
    def setUp(self):
        Currency.objects.all().delete()
        obj = mixer.blend('exchange_backend.Currency', name="Testcurrs")
        obj = mixer.blend('exchange_backend.Currency', name="INR")

    def test_create(self):
        curr_obj = Currency.objects.filter(name="Testcurrs").first()

        self.assertEqual(curr_obj.name, "Testcurrs")

    def test_print(self):
        curr_obj = Currency.objects.filter(name="INR").first()
        self.assertEqual(curr_obj.__str__(), "INR")

    def test_create_name(self):
        curr_obj = Currency.objects.filter(name="INR").first()
        self.assertEqual(curr_obj.name, "INR")


class TestWallet(TestCase):
    def setUp(self):
        obj = mixer.blend('exchange_backend.Currency', name="Testcurrs")
        obj = mixer.blend('exchange_backend.Wallet', currency_type=obj)
        obj = mixer.blend('exchange_backend.Currency', name="INR")
        obj = mixer.blend('exchange_backend.Wallet', currency_type=obj)

    def test_create(self):
        self.assertGreaterEqual(Wallet.objects.count(), 0), 'Checking the added record in DB'

    def test_create_data(self):
        curr_obj = mixer.blend('exchange_backend.Currency', name="INR")
        obj = mixer.blend('exchange_backend.Wallet', current_balance=100, currency_type=curr_obj)
        assert obj.current_balance == 100.0, 'Checking the added record in DB has given value in name column'
        assert obj.currency_type.id == curr_obj.pk, 'Checking the added record in DB has given foreign key relation'

    def test_create_none(self):
        kwargs = {"current_balance": None}
        self.assertRaises(ValidationError, mixer.blend, 'exchange_backend.Wallet', **kwargs)


class TestUser(TestCase):
    def setUp(self):
        obj = mixer.blend('exchange_backend.User')
        self.wallet_obj = mixer.blend('exchange_backend.Wallet')
        self.curr_obj = mixer.blend('exchange_backend.Currency')
        self.new_curr_obj = mixer.blend('exchange_backend.Currency')
        user_obj = mixer.blend('exchange_backend.User', username="testuser", first_name="test", wallet=self.wallet_obj,
                               default_currency=self.curr_obj)

    def test_create(self):
        user_obj = User.objects.filter(username="testuser").first()
        self.assertEqual(user_obj.first_name, "test")
        self.assertGreater(User.objects.count(), 0)

    def test_create_data(self):
        user_obj = User.objects.filter(username="testuser").first()
        self.assertEqual(user_obj.default_currency.id, self.curr_obj.id)
        self.assertEqual(user_obj.wallet, self.wallet_obj)



    def test_create_default_values(self):
        user_obj = mixer.blend('exchange_backend.User', wallet=None, default_currency=None)
        User.create_default_values(user_obj)
        self.assertEqual(user_obj.default_currency.name, "INR")
        User.create_default_values(user_obj)
        self.assertEqual(user_obj.default_currency.name, "INR")

    #
    def test_user_postsave(self):
        wallet_obj = mixer.blend("exchange_backend.Wallet")
        user_obj = User.objects.create(username="test", password="test@123", default_currency=self.curr_obj,
                                       wallet=wallet_obj)
        user_obj = User.objects.filter(username="test").first()
        user_obj.username = "test2"
        user_obj.default_currency = self.new_curr_obj
        user_obj.save()
        user_obj.save()

    def test_update_currency(self):
        wallet_obj = mixer.blend('exchange_backend.Wallet')
        curr_obj = mixer.blend('exchange_backend.Currency')
        user_obj = User.objects.create(username="test", password="test@123", wallet=wallet_obj)
        User.create_default_values(user_obj)
        user_obj.default_currency.name = "GBP"
        user_obj.save()
        self.assertEqual(user_obj.wallet.currency_type.name, "INR")


class TestTransaction(TestCase):
    def setUp(self) -> None:
        self.wallet_obj = mixer.blend('exchange_backend.Wallet')
        self.user_obj = mixer.blend('exchange_backend.User', wallet=self.wallet_obj)
        self.curr_obj = mixer.blend('exchange_backend.Currency')

    def test_create(self):
        obj = mixer.blend('exchange_backend.Transaction', wallet=self.wallet_obj,user=self.user_obj)
        assert obj.pk == 1, 'Checking the added record in DB'

    def test_create_data(self):

        trans_obj = Transaction.objects.create(transaction_type="debit", currency_type=self.curr_obj,
                                user=self.user_obj, amount=100)
        trans_obj.save()
        self.assertEqual(trans_obj.transaction_type, "debit")
        self.assertEqual(trans_obj.user.id, self.user_obj.pk)

    def test_create_none(self):
        try:
            obj = mixer.blend('exchange_backend.Transaction', user=None)
        except ValidationError as e:
            assert True, 'Checking the added record in DB has given value in user'
        else:
            assert False
