from django.urls import path
from apps.orders.views import OrderCreateFromCartView, OrderDetailView

urlpatterns = [
    path("", OrderCreateFromCartView.as_view(), name="order-create-from-cart"),
    path("<int:order_id>/", OrderDetailView.as_view(), name="order-detail"),
]
