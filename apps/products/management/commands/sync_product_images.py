from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from apps.products.models import Product, ProductImage  # ou apps.products.models selon ton import

class Command(BaseCommand):
    def handle(self, *args, **options):
        media_dir = Path(settings.MEDIA_ROOT) / "products" / "images"
        ext_map = {p.stem: p.name for p in media_dir.glob("*")}
        updated = 0
        for product in Product.objects.all():
            filename = ext_map.get(product.slug)
            if not filename:
                continue
            image_path = f"products/images/{filename}"
            img = product.images.order_by("sort_order", "id").first()
            if img:
                img.image, img.alt_text = image_path, product.title
                img.save()
            else:
                ProductImage.objects.create(product=product, image=image_path,
                                            alt_text=product.title, sort_order=0)
            updated += 1
        self.stdout.write(self.style.SUCCESS(f"OK: {updated} images synchronisées"))