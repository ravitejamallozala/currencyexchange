from rest_framework import routers
from django.conf.urls import url, include
from . import views
from .views import RegisterView, TransferView, AddmoneyView

router = routers.DefaultRouter()
router.register(r"user", views.UserViewSet, base_name="user")
router.register(r"wallet", views.WalletViewset, base_name="wallet")
router.register(r"currency", views.CurrencyViewset, base_name="currency")
router.register(r"transaction", views.TransactionViewset, base_name="transaction")

urlpatterns = [
    url("^api/", include(router.urls)),
    url(r"^login/$", views.LoginView.as_view(), name="login"),
    url(r"^logout/$", views.LogoutView.as_view(), name="logout"),
    url(r"^register/$", RegisterView.as_view(), name='register'),
    url(r"^transfer_view/$", TransferView.as_view(), name='transfer_view'),
    url(r"^addmoney/$", AddmoneyView.as_view(), name='addmoney'),
    url(r"^.+/", views.ServeFrontend.as_view(), name="serve_frontend"),
    url(r"^$", views.ServeFrontend.as_view(), name="serve_frontend"),
]

