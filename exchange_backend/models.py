import django
from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth import models as auth_models
from models_common import NAME_LENGTH
from model_utils import Choices


class Currency(models.Model):
    name = models.CharField(max_length=NAME_LENGTH)


class Wallet(models.Model):
    current_balance = models.FloatField(default=0.0)
    currency_type = models.ForeignKey(Currency)


class User(auth_models.AbstractUser):
    wallet = models.OneToOneField(Wallet, related_name="user_wallet")
    default_currency = models.ForeignKey(Currency)
    profile_image = models.FileField(
        upload_to="profile_images/",
        validators=[FileExtensionValidator(allowed_extensions=["jpeg", 'jpg', 'png'])],
    )


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = Choices(("debit", "debit"), ("credit", "credit"), ("transfer", "transfer"))
    STATUS_CHOICES = Choices(("accepted", "accepted"), ("declined", "declined"))

    user = models.ForeignKey(User, related_name="transaction")
    dest_user_id = models.IntegerField(blank=True, null=True)
    transaction_type = models.CharField(
        max_length=NAME_LENGTH, choices=TRANSACTION_TYPE_CHOICES,
    )
    amount = models.FloatField()
    timestamp = models.DateTimeField(default=django.utils.timezone.now)
    currency_type = models.ForeignKey(Currency)
    remaining_balance = models.FloatField(blank=True, null=True)
    status = models.CharField(
        max_length=NAME_LENGTH, choices=STATUS_CHOICES, blank=True, null=True,
    )
    description = models.CharField(
        max_length=NAME_LENGTH, blank=True, null=True
    )
