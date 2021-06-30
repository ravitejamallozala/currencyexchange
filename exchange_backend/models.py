import django
from django.core.validators import FileExtensionValidator
from django.db import models, transaction
from django.contrib.auth import models as auth_models

from models_common import NAME_LENGTH, ExchangeBaseModel
from model_utils import Choices
from django.db.models.signals import post_save


class Currency(ExchangeBaseModel):
    name = models.CharField(max_length=NAME_LENGTH)

    def __str__(self):
        return self.name


class Wallet(ExchangeBaseModel):
    current_balance = models.FloatField(default=0.0)
    currency_type = models.ForeignKey(Currency)


class User(auth_models.AbstractUser, ExchangeBaseModel):
    wallet = models.OneToOneField(Wallet, related_name="user_wallet", blank=True, null=True)
    default_currency = models.ForeignKey(Currency, blank=True, null=True)
    profile_image = models.FileField(
        upload_to="profile_images/",
        validators=[FileExtensionValidator(allowed_extensions=["jpeg", 'jpg', 'png'])], blank=True, null=True
    )

    class Meta:
        fetch_old_instance = True

    @staticmethod
    def create_default_values(instance):
        from exchange_backend.serializers import WalletSerializer
        if not instance.default_currency:
            currency_obj = Currency.objects.get_or_create(name="INR")[0] # Assuming INR to be default currency of user
            instance.default_currency = currency_obj
        else:
            currency_obj = instance.default_currency
        wser = WalletSerializer(
            data={
                "current_balance": 0.0,
                "currency_type": currency_obj.id,
            }
        )
        wser.is_valid(raise_exception=True)
        w_obj = wser.save()
        instance.wallet = w_obj
        instance.save()

    @classmethod
    def post_save(cls, sender, instance, created, *args, **kwargs):
        print("Here in User postsave")
        if created:
            transaction.on_commit(lambda: cls.create_default_values(instance))
        else:
            from exchange_backend.views import ExchangeService
            old_instance = instance.old_instance
            print(old_instance)
            if not old_instance:
                return
            if old_instance.default_currency != instance.default_currency:
                wallet_obj = instance.wallet
                converted_value = ExchangeService.convert_currency(old_instance.default_currency.name,
                                                                   instance.default_currency.name,
                                                                   wallet_obj.current_balance)
                wallet_obj.current_balance = converted_value
                wallet_obj.currency_type = instance.default_currency
                wallet_obj.save()


models.signals.post_save.connect(User.post_save, sender=User)


class Transaction(ExchangeBaseModel):
    TRANSACTION_TYPE_CHOICES = Choices(("debit", "debit"), ("credit", "credit"), ("transfer", "transfer"))
    STATUS_CHOICES = Choices(("accepted", "accepted"), ("declined", "declined"))

    user = models.ForeignKey(User, related_name="transaction")
    dest_user_id = models.IntegerField(blank=True, null=True)
    transaction_type = models.CharField(
        max_length=NAME_LENGTH, choices=TRANSACTION_TYPE_CHOICES,
    )
    amount = models.FloatField()
    timestamp = models.DateTimeField(default=django.utils.timezone.now)  # noqa
    currency_type = models.ForeignKey(Currency)
    remaining_balance = models.FloatField(blank=True, null=True)
    status = models.CharField(
        max_length=NAME_LENGTH, choices=STATUS_CHOICES, blank=True, null=True,
    )
    description = models.CharField(
        max_length=NAME_LENGTH, blank=True, null=True
    )

    @classmethod
    def post_save(cls, sender, instance, created, *args, **kwargs):
        # Update remaining balance here
        if created:
            wallet = instance.user.wallet
            instance.remaining_balance = wallet.current_balance
            instance.save()


models.signals.post_save.connect(User.post_save, sender=User)
