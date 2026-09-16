from django.urls import path

from apps.accounts.views import AccountListView

urlpatterns = [
    path("", AccountListView.as_view(), name="account-list"),
]