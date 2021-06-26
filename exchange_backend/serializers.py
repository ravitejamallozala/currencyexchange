from django.contrib.auth.models import Group
from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField
from rest_framework import serializers
from exchange_backend import models


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Currency
        fields = "__all__"


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()


class WalletSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(read_only=True)

    class Meta:
        model = models.Wallet
        fields = "__all__"


class GroupSerializerlite(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = ("permissions",)


class UserSerializer(serializers.ModelSerializer):
    groups = PresentablePrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        presentation_serializer=GroupSerializerlite,
        many=True,
    )
    wallet = WalletSerializer(read_only=True)
    wallet_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Wallet.objects.all(), write_only=True, source="wallet",
    )
    currency = CurrencySerializer(read_only=True)
    currency_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Currency.objects.all(), write_only=True, source="currency",
    )

    class Meta:
        model = models.User
        exclude = (
            "is_staff",
            "user_permissions",
        )
        read_only_fields = (
            "is_superuser",
            "is_active",
            "date_joined",
        )
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
        }


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = "__all__"
