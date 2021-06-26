from django.contrib import admin
from easy_select2 import select2_modelform
from exchange_backend import models
from admin_common import ff
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin


class UserCreateForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = ("username", "email")


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    add_form = UserCreateForm


class CurrencyAdmin(admin.ModelAdmin):
    form = select2_modelform(models.Currency)
    list_display = ("id", "name")
    search_fields = ("id", "name")


class WalletAdmin(admin.ModelAdmin):
    form = select2_modelform(models.Wallet)
    list_display = ("id", "current_balance", ff("currency_type__name"))
    search_fields = ("id", "current_balance", ff("currency_type__name"))


class TransactionAdmin(admin.ModelAdmin):
    form = select2_modelform(models.Transaction)
    list_display = (
        "id", ff("user__id"), "dest_user_id",  "amount", "status", ff("currency_type__name"))

    search_fields = (
        "id", "dest_user_id", "amount", "status", ff("currency_type__name"))



admin.site.register(models.Currency, CurrencyAdmin)
admin.site.register(models.Wallet, WalletAdmin)
admin.site.register(models.Transaction, TransactionAdmin)
