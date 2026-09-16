from django.urls import path
from apps.payments.views import PaymentConfirmView, PaymentCreateView

urlpatterns = [
    path("", PaymentCreateView.as_view(), name="payment-create"),
    path("<int:payment_id>/confirm/", PaymentConfirmView.as_view(), name="payment-confirm"),
]
