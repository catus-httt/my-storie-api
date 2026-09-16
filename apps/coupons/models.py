from config import settings
from django.db import models
from django.utils import timezone

from apps.orders.models import Order


class Coupon(models.Model):
    DISCOUNT_PERCENT = "percent"
    DISCOUNT_FIXED = "fixed"

    DISCOUNT_TYPE_CHOICES = [
        (DISCOUNT_PERCENT, "Percent"),
        (DISCOUNT_FIXED, "Fixed amount"),
    ]

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)

    max_redemptions = models.PositiveIntegerField(null=True, blank=True)
    redeemed_count = models.PositiveIntegerField(default=0)

    min_order_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()

    is_active = models.BooleanField(default=True)

    def is_valid(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if self.valid_from > now or self.valid_until < now:
            return False
        if self.max_redemptions and self.redeemed_count >= self.max_redemptions:
            return False
        return True

    def __str__(self):
        return self.code


class CouponRedemption(models.Model):
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.CASCADE,
        related_name="redemptions",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="coupon_redemptions",
    )
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="coupon_redemption",
    )
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    redeemed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("coupon", "user", "order")