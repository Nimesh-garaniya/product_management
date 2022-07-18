"""
    Used to manage all the URL's related to User Account
"""
from django.urls import path

from account.views import activate, UserRegisterView, LoginView, LogoutView

app_name = "account"

urlpatterns = [
    path("", UserRegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), {'redirect_if_logged_in': '/product_view'}, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # path("home/", HomeView.as_view(), name="home"),
    path(
        "activate/^(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/",
        activate,
        name="activate",
    ),
]
