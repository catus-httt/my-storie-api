from rest_framework import serializers

from apps.payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "status",
            "provider",
            "amount",
            "currency",
            "provider_payment_id",
            "checkout_url",
            "created_at",
            "updated_at",
        ]
