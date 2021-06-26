from django.shortcuts import render
from rest_framework.decorators import list_route

from exchange_backend import filters
from serializers import *
from views_common import *
from models import Currency


class CurrencyViewset(ExchangeModelViewSet):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()
    filter_class = filters.CurrencyFilter
    ordering_fields = ("id", "name")
    search_fields = ("id", "name")


class UserViewSet(ExchangeModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        queryset = super(UserViewSet, self).get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(id=self.request.user.id)

    @list_route(methods=["get"])
    def currentuser(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)


class WalletViewset(ExchangeModelViewSet):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()
    filter_class = filters.WalletFilter
    ordering_fields = (
        "id",
        "current_balance",
        "currency_type"
    )
    search_fields = (
        "id",
        "current_balance",
        "currency_type"
    )


class TransactionViewset(ExchangeModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    filter_class = filters.TransactionFilter
    ordering_fields = (
        "id",
        "status",
        "amount",
        "transaction_type",
        "currency_type",
    )
    search_fields = (
        "id",
        "status",
        "amount",
        "transaction_type",
        "currency_type",
    )
