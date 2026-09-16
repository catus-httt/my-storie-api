from rest_framework import serializers

from apps.orders.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product_title",
            "variant_name",
            "quantity",
            "unit_price",
            "total_price",
            "is_digital",
            "is_physical",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "subtotal",
            "discount_amount",
            "total_amount",
            "billing_address",
            "shipping_address",
            "items",
            "created_at",
            "paid_at",
        ]
