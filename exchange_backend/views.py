from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.shortcuts import render
from django.views.generic.base import TemplateResponseMixin, View, TemplateView
from rest_framework.decorators import list_route, authentication_classes, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework.generics import get_object_or_404, CreateAPIView
import requests
from rest_framework.views import APIView

from exchange_backend import filters
from misc import IsAuthenticatedOrOptions
from .serializers import *
from views_common import *
from .models import Currency, Wallet, Transaction, User


class RegisterView(CreateAPIView, TemplateResponseMixin):
    template_name = "signup.html"
    redirect_field_name = REDIRECT_FIELD_NAME
    queryset = User.objects.all()
    permission_classes = (IsAuthenticatedOrOptions,)
    serializer_class = RegisterSerializer

    def get(self, request):
        return self.render_to_response({})

    def post(self, request, *args, **kwargs):
        redirect_to = request.POST.get(
            self.redirect_field_name, request.GET.get(self.redirect_field_name, ""),
        )

        self.create(request, *args, **kwargs)
        final_response = HttpResponseRedirect(redirect_to)
        print(final_response)
        return final_response


class ServeFrontend(View, TemplateResponseMixin):
    # TODO roman add permission
    template_name = "base.html"
    permission_classes = [IsAuthenticatedOrOptions]

    def get(self, request):
        return self.render_to_response({})


class TransferView(View, TemplateResponseMixin):
    # TODO roman add permission
    template_name = "transfer.html"
    permission_classes = [IsAuthenticatedOrOptions]

    def get(self, request):
        currencies = Currency.objects.all()
        users = User.objects.all()
        return self.render_to_response({
            "user": request.user if request.user else None,
            "currencies": currencies,
            "users": users
        })


class AddmoneyView(View, TemplateResponseMixin):
    # TODO roman add permission
    template_name = "add_money.html"
    permission_classes = [IsAuthenticatedOrOptions]

    def get(self, request):
        currencies = Currency.objects.all()
        users = User.objects.all()
        return self.render_to_response({
            "user": request.user if request.user else None,
            "currencies": currencies,
            "users": users
        })


class WithdrawmoneyView(View, TemplateResponseMixin):
    # TODO roman add permission
    template_name = "withdraw_money.html"
    permission_classes = [IsAuthenticatedOrOptions]

    def get(self, request):
        currencies = Currency.objects.all()
        users = User.objects.all()
        return self.render_to_response({
            "user": request.user if request.user else None,
            "currencies": currencies,
            "users": users
        })


class ProfileView(View, TemplateResponseMixin):
    # TODO roman add permission
    template_name = "profile.html"
    permission_classes = [IsAuthenticatedOrOptions]

    def get(self, request):
        users = User.objects.all()
        return self.render_to_response({
            "user": request.user
        })


@authentication_classes([])
@permission_classes([])
class LoginView(APIView, TemplateResponseMixin):
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = "login.html"

    def get(self, request):

        return self.render_to_response({})

    def post(self, request):
        redirect_to = request.POST.get(
            self.redirect_field_name, request.GET.get(self.redirect_field_name, ""),
        )
        username = request.data['username']
        password = request.data['password']
        serializer = LoginSerializer(data={"username": username, "password": password})
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data["username"].lower(),
                password=serializer.validated_data["password"],
            )
            if not user:
                return Response(
                    status=401, data={"error": True, "authentication": False},
                )
            login(request, user)
            final_response = HttpResponseRedirect(redirect_to)
            return final_response
        return Response(status=401, data={"error": True, "authentication": False})


class LogoutView(APIView):
    redirect_field_name = REDIRECT_FIELD_NAME
    permission_classes = (IsAuthenticatedOrOptions,)

    def get(self, request):
        redirect_to = request.POST.get(
            self.redirect_field_name, request.GET.get(self.redirect_field_name, ""),
        )
        final_response = HttpResponseRedirect(redirect_to)
        logout(request)
        return final_response

    def post(self, request):
        redirect_to = request.POST.get(
            self.redirect_field_name, request.GET.get(self.redirect_field_name, ""),
        )
        final_response = HttpResponseRedirect(redirect_to)
        logout(request)
        return final_response


class CurrencyViewset(ExchangeModelViewSet):
    serializer_class = CurrencySerializer
    permission_classes = [IsAuthenticatedOrOptions]
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
        value = 0
        req_obj = requests.get(url=url, params=params)
        if req_obj.status_code == 200:
            data = req_obj.json()
            if converstion_string in data:
                value = amount * data[converstion_string]
        """We can roundoff the converted value to floating point precision 2"""
        # return round(value, 2)
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

    @staticmethod
    def withdraw_money(user, currency_obj, amount, is_transfer=False):
        if user.default_currency.id != currency_obj.id:
            amount = ExchangeService.convert_currency(currency_obj.name, user.default_currency.name, float(amount))
        validation = WalletViewset.validate_debit(user, amount)
        if not validation:
            raise ValidationError(f"Amount cannot be Withdrawn as Balance is lesser than withdrawing amount ")
        if not is_transfer:
            tser = TransactionSerializer(data={
                "user": user.id,
                "dest_user_id": None,
                "transaction_type": "debit",
                "amount": -amount,
                "currency_type": currency_obj.id,
                "status": "accepted",
                "description": None,
            })
            tser.is_valid(raise_exception=True)
            tser.save()
        with transaction.atomic():
            wallet_obj = Wallet.objects.filter(user_wallet=user.id).select_for_update()
            wallet_obj = wallet_obj.first()
            wallet_obj.current_balance -= amount
            wallet_obj.save()
        return

    @staticmethod
    def add_money(user, currency_obj, amount, is_transfer=False):
        if user.default_currency.id != currency_obj.id:
            amount = ExchangeService.convert_currency(currency_obj.name, user.default_currency.name, amount)
        if not is_transfer:
            tser = TransactionSerializer(data={
                "user": user.id,
                "dest_user_id": None,
                "transaction_type": "credit",
                "amount": amount,
                "currency_type": currency_obj.id,
                "status": "accepted",
                "description": None,
            })
            tser.is_valid(raise_exception=True)
            tser.save()
        with transaction.atomic():
            wallet_obj = Wallet.objects.filter(user_wallet=user.id).select_for_update()
            wallet_obj = wallet_obj.first()
            wallet_obj.current_balance += amount
            wallet_obj.save()
        return

    @staticmethod
    def transfer_money(from_user, to_user, amount, currency_obj):
        if from_user.default_currency.id != currency_obj.id:
            amount = ExchangeService.convert_currency(currency_obj.name, from_user.default_currency.name, amount)
            validation = WalletViewset.validate_debit(from_user, amount)
            if not validation:
                raise ValidationError(f"Amount cannot be Transferred as Balance is lesser than transfering amount")
        tser = TransactionSerializer(data={
            "user": from_user.id,
            "dest_user_id": to_user.id,
            "transaction_type": "transfer",
            "amount": amount,
            "currency_type": currency_obj.id,
            "status": "accepted",
            "description": None,
        })
        tser.is_valid(raise_exception=True)
        # tser.save()
        with transaction.atomic():
            WalletViewset.withdraw_money(from_user, from_user.default_currency, amount, True)
            WalletViewset.add_money(to_user, from_user.default_currency, amount, True)

    @classmethod
    def validate_debit(cls, user, amount):
        wallet = user.wallet
        if wallet.current_balance < amount:
            return False
        return True


class TransactionViewset(ExchangeModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()  # noqa
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

    @transaction_atomic_db
    @list_route(methods=['post'])
    def wallet_transaction(self, request):
        amount = request.data.get("amount", None)
        currency_id = request.data.get("currency", None)
        transaction_type = request.data.get("transaction_type", None)
        if transaction_type not in Transaction.TRANSACTION_TYPE_CHOICES:
            return Response(status=400, data={"message": "Transaction Invalid"})
        curr_obj = get_object_or_404(Currency, pk=int(currency_id))
        # if not curr_obj:
        #     return Response(status=400, data={"message": "Transaction Invalid"})
        status = None
        if transaction_type == "debit":
            WalletViewset.withdraw_money(request.user, curr_obj, float(amount), False)
            # raise Exception
            return Response(status=200,
                            data={"message": "Money Successfully Debited from your Wallet"})
        elif transaction_type == "credit":
            WalletViewset.add_money(request.user, curr_obj, float(amount), False)
            return Response(status=200,
                            data={"message": "Money Successfully Credited to your Wallet"})

    from django.views.decorators.csrf import csrf_exempt
    @csrf_exempt
    @transaction_atomic_db
    @list_route(methods=['post'])
    def transfer_money(self, request):
        amount = request.data.get("amount", None)
        currency_id = request.data.get("currency", None)
        # from_user_id = request.data.get("from_user_id", None)
        from_user_id = request.user.id
        to_user_id = request.data.get("to_user_id", None)
        if not amount or not currency_id or not from_user_id or not to_user_id:
            return Response(status=400,
                            data={"message": "Bad Request"})
        from_user = get_object_or_404(User, pk=int(from_user_id))
        to_user = get_object_or_404(User, pk=int(to_user_id))
        curr_obj = get_object_or_404(Currency, pk=int(currency_id))
        WalletViewset.transfer_money(from_user, to_user, float(amount), curr_obj)
        return Response(status=200, data={"message": "Money Successfully Transfered"})
