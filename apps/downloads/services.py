from datetime import timedelta

from django.utils import timezone

from apps.downloads.models import DownloadAccess


def grant_download_access_for_order(order):
    for item in order.items.select_related("product"):
        if not item.is_digital:
            continue

        product_files = item.product.files.filter(is_preview=False)

        for product_file in product_files:
            DownloadAccess.objects.get_or_create(
                user=order.user,
                order=order,
                order_item=item,
                product_file=product_file,
                defaults={
                    "max_downloads": 5,
                    "expires_at": timezone.now() + timedelta(days=365),
                },
            )