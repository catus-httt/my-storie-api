from django.db import models
from django.utils.text import slugify
from django.conf import settings

class ProductCategory(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)

    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="children",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    
class ProductTag(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    PRODUCT_TYPE_DIGITAL = "Digital"
    PRODUCT_TYPE_PHYSICAL = "Physical"
    PRODUCT_TYPE_BOTH = "Both"

    PRODUCT_TYPE_CHOICES = [(PRODUCT_TYPE_DIGITAL, "Digital file"), (PRODUCT_TYPE_PHYSICAL, "Printed physical product"), (PRODUCT_TYPE_BOTH, "Digital and Physical product")]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()

    product_category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, related_name="products")
    product_tag = models.ManyToManyField(ProductTag, blank=True, related_name="products")

    base_price = models.DecimalField(max_digits=10, decimal_places=2) 
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES, default=PRODUCT_TYPE_DIGITAL)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="products")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Product : {self.title}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/images/")
    alt_text = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Image for {self.product.title}"

    

class ProductFile(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="products/files/")
    file_name = models.CharField(max_length=255)
    file_size = models.PositiveBigIntegerField(default=0)
    file_format = models.CharField(max_length=30, blank=True)
    is_preview = models.BooleanField(default=False)

    def __str__(self):
        return self.file_name
    

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    name = models.CharField(max_length=120)
    sku = models.CharField(max_length=80, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.product.title} - {self.name}"
    

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="product_reviews")
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    class Meta:
        unique_together = ("product", "user")

    def __str__(self):
        return f"{self.product.title} - {self.rating}"