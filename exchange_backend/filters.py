import rest_framework_filters as filters
from . import models


class CurrencyFilter(filters.FilterSet):
    id = filters.AllLookupsFilter(name="id")
    name = filters.AllLookupsFilter(name="name")

    class Meta:
        model = models.Currency
        fields = ["id", "name"]


class WalletFilter(filters.FilterSet):
    id = filters.AllLookupsFilter(name="id")
    current_balance = filters.AllLookupsFilter(name="current_balance")
    currency_type = filters.RelatedFilter(
        CurrencyFilter, queryset=models.Currency.objects.all(),
    )

    class Meta:
        model = models.Wallet
        fields = ["id", "current_balance"]


class UserFilter(filters.FilterSet):
    id = filters.AllLookupsFilter(name="id")
    username = filters.AllLookupsFilter(name="username")
    default_currency = filters.RelatedFilter(
        CurrencyFilter, queryset=models.Currency.objects.all(),
    )

    class Meta:
        model = models.User
        fields = ["id", "username"]


class TransactionFilter(filters.FilterSet):
    id = filters.AllLookupsFilter(name="id")
    dest_user_id = filters.AllLookupsFilter(name="dest_user_id")
    transaction_type = filters.AllLookupsFilter(name="transaction_type")
    amount = filters.AllLookupsFilter(name="amount")
    status = filters.AllLookupsFilter(name="status")
    user = filters.RelatedFilter(
        UserFilter, queryset=models.User.objects.all(),
    )
    currency_type = filters.RelatedFilter(
        CurrencyFilter, queryset=models.Currency.objects.all(),
    )

    class Meta:
        model = models.Transaction
        fields = ["id", "transaction_type", "dest_user_id", "amount", "status"]
