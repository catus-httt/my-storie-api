from django.db import models
from django.conf import settings
from apps.products.models import Product, ProductVariant

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_amount(self):
        return sum(item.subtotal for item in self.items.all())
    
def __str__(self):
        return f"Cart of {self.user.email}"
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def unit_price(self):
        if self.variant:
            return self.variant.price
        return self.product.base_price
    
    @property
    def subtotal(self):
        return self.unit_price * self.quantity
    
    class Meta:
        unique_together = ("cart", "product", "variant")
    
    def __str__(self):
        return f"{self.quantity} x {self.product.title}"