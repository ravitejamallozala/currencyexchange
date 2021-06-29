from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from exchange_backend import models
from exchange_backend.models import User


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'password')


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )

        user.set_password(validated_data['password'])
        user.groups.add(1)
        user.save()
        return user


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Currency
        fields = "__all__"


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
