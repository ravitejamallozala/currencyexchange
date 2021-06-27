from rest_framework import routers
from django.conf.urls import url, include
from . import views
from .views import RegisterView

router = routers.DefaultRouter()
router.register(r"user", views.UserViewSet, base_name="user")
router.register(r"wallet", views.WalletViewset, base_name="wallet")
router.register(r"currency", views.CurrencyViewset, base_name="currency")
router.register(r"transaction", views.TransactionViewset, base_name="transaction")

urlpatterns = [
    url("^api/", include(router.urls)),
    url(r"^login/$", views.LoginView.as_view(), name="login"),
    url(r"^logout/$", views.LogoutView.as_view(), name="logout"),
    url('register/', RegisterView.as_view(), name='register'),

    # url(
    #     r"^login_background_image/$",
    #     views.LoginBackgroundImage.as_view(),
    #     name="login_background_image",
    # ),
    # url(r"^.+/", views.ServeFrontend.as_view(), name="serve_frontend"),
    # url(r"^$", views.ServeFrontend.as_view(), name="serve_frontend"),
]

