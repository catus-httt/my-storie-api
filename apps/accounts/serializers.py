from rest_framework import serializers

from apps.accounts.models import CustomerProfile

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ["user", "phone", "billing_address", "shipping_address"]