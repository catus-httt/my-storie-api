from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.orders.models import Order, OrderItem
from apps.products.models import ProductFile


class DownloadAccess(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="download_accesses",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="download_accesses",
    )
    order_item = models.ForeignKey(
        OrderItem,
        on_delete=models.CASCADE,
        related_name="download_accesses",
    )
    product_file = models.ForeignKey(
        ProductFile,
        on_delete=models.CASCADE,
        related_name="download_accesses",
    )

    max_downloads = models.PositiveIntegerField(default=5)
    download_count = models.PositiveIntegerField(default=0)
    expires_at = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def can_download(self):
        if not self.is_active:
            return False
        if self.download_count >= self.max_downloads:
            return False
        if self.expires_at and timezone.now() > self.expires_at:
            return False
        return True


class DownloadLog(models.Model):
    access = models.ForeignKey(
        DownloadAccess,
        on_delete=models.CASCADE,
        related_name="logs",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    downloaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Download by {self.user.email}"