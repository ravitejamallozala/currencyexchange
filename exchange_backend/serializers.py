from django.contrib.auth.models import Group
from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField
from rest_framework import serializers
from models import *


class CurrencySerializer(serializers.Serializer):
    class Meta:
        model = Currency
        fields = "__all__"


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class WalletSerializer(serializers.Serializer):
    class Meta:
        model = Wallet
        fields = "__all__"


class GroupSerializerlite(serializers.Serializer):
    class Meta:
        model = Group
        exclude = ("permissions",)


class UserSerializer(serializers.Serializer):
    groups = PresentablePrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        presentation_serializer=GroupSerializerlite,
        many=True,
    )
    wallet = Wallet(read_only=True)
    wallet_id = serializers.PrimaryKeyRelatedField(
        queryset=Wallet.objects.all(), write_only=True, source="wallet",
    )
    currency = Currency(read_only=True)
    currency_id = serializers.PrimaryKeyRelatedField(
        queryset=Currency.objects.all(), write_only=True, source="currency",
    )

    class Meta:
        model = User
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


class TransactionSerializer(serializers.Serializer):
    class Meta:
        model = Transaction
        fields = "__all__"
