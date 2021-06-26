from django.shortcuts import render
from rest_framework.decorators import list_route
from rest_framework.response import Response
from django.http import HttpResponseRedirect, HttpResponse
import requests
from exchange_backend import filters
from .serializers import *
from views_common import *
from .models import Currency, Wallet, Transaction, User


class CurrencyViewset(ExchangeModelViewSet):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()
    filter_class = filters.CurrencyFilter
    ordering_fields = ("id", "name")
    search_fields = ("id", "name")

    @list_route()
    def populate_currencies(self, request):
        currencies_list = ExchangeService.get_all_currencies()
        for curr in currencies_list:
            Currency.objects.get_or_create(name=curr)
        return Response(status=200, data={"message": "Currencies Successfully Populated"})


class ExchangeService:
    @staticmethod
    def get_all_currencies():
        url = settings.EXCHANGE_API['BASE_URL']
        url = f"{url}{settings.EXCHANGE_API['LIST_CURRENCIES_API']}"
        params = {
            "apiKey": {settings.EXCHANGE_API['API_TOKEN']}
                  }
        req_obj = requests.get(url=url, params=params)
        currencies_list = []
        if req_obj.status_code == 200:
            data = req_obj.json()
            print(data['results'])
            currencies_list = list(data['results'].keys()) if 'results' in data else []
        return currencies_list

    @staticmethod
    def convert_currency(base_currency, to_currency, amount):
        url = f"{settings.EXCHANGE_API['BASE_URL']}{settings.EXCHANGE_API['CONVERT_API']}"
        converstion_string = f"{base_currency}_{to_currency}"
        params = {
            "q": converstion_string,
            "compact": "ultra",
            "apiKey": {settings.EXCHANGE_API['API_TOKEN']}
        }
        value = None
        req_obj = requests.get(url=url, params=params)
        if req_obj.status_code == 200:
            data = req_obj.json()
            print(data)
            # if converstion_string in data:
            value = amount * data[converstion_string]
        return value


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
