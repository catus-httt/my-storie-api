from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.views import get_user_cart, get_checkout_user
from apps.orders.models import Order, OrderItem
from apps.orders.serializers import OrderSerializer


class OrderCreateFromCartView(APIView):
    @transaction.atomic
    def post(self, request):
        user = get_checkout_user(request)
        cart = get_user_cart(request)
        cart_items = list(cart.items.select_related("product", "variant"))

        if not cart_items:
            return Response({"message": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        subtotal = sum(item.subtotal for item in cart_items)
        billing_address = request.data.get("billing_address", "")
        shipping_address = request.data.get("shipping_address", "")

        order = Order.objects.create(
            user=user,
            subtotal=subtotal,
            discount_amount=0,
            total_amount=subtotal,
            billing_address=billing_address,
            shipping_address=shipping_address,
        )

        for cart_item in cart_items:
            product_type = cart_item.product.product_type
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                variant=cart_item.variant,
                product_title=cart_item.product.title,
                variant_name=cart_item.variant.name if cart_item.variant else "",
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                total_price=cart_item.subtotal,
                is_digital=product_type in ["Digital", "Both"],
                is_physical=product_type in ["Physical", "Both"],
            )

        cart.items.all().delete()

        serializer = OrderSerializer(order, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailView(APIView):
    def get(self, request, order_id):
        user = get_checkout_user(request)
        order = Order.objects.prefetch_related("items").get(id=order_id, user=user)
        serializer = OrderSerializer(order, context={"request": request})
        return Response(serializer.data)
