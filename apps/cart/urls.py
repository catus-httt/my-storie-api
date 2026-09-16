from django.urls import path
from apps.cart.views import CartAddItemView, CartDetailView, CartItemUpdateView

urlpatterns = [
    path("", CartDetailView.as_view(), name="cart-detail"),
    path("items/", CartAddItemView.as_view(), name="cart-add-item"),
    path("items/<int:item_id>/", CartItemUpdateView.as_view(), name="cart-update-item"),
]
