from django.db import models
from apps.orders.models import Order

class Payment(models.Model):
    STATUS_PENDING = "pending"
    STATUS_SUCCEDED = "succeded"
    STATUS_FAILED = "failed"
    STATUS_CANCELED = "canceled"

    PROVIDER_STRIPE = "Stripe"
    PROVIDER_PAYPAL = "Paypal"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_SUCCEDED, "Succeded"),
        (STATUS_FAILED, "Failed"),
        (STATUS_CANCELED, "Canceled")
    ]

    PROVIDER_CHOICES = [
        (PROVIDER_STRIPE, "Stripe"),
        (PROVIDER_PAYPAL, "Paypal")
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_PENDING)
    provider = models.CharField(max_length=30, choices=PROVIDER_CHOICES)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="EUR")

    provider_payment_id = models.CharField(max_length=255, blank=True)
    # URL mà provider trả về để user click vào và payer
    checkout_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class PaymentEvent(models.Model):
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name="events",
        null=True,
        blank=True,
    )
    provider = models.CharField(max_length=30)
    event_type = models.CharField(max_length=120)
    event_id = models.CharField(max_length=255, unique=True)
    payload = models.JSONField()
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.provider} - {self.event_type}"