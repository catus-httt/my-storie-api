from rest_framework import serializers

from apps.products.models import Product, ProductCategory, ProductTag, ProductImage, ProductVariant

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["id", "name", "slug"]

class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = ["id", "name", "slug"]

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "alt_text", "sort_order"]

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ["id", "name", "sku", "price", "stock_quantity", "is_active"]

class ProductSerializer(serializers.ModelSerializer):
    product_category = ProductCategorySerializer(read_only=True)
    product_tag = ProductTagSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "title", "slug", "description", "base_price",
            "is_active", "is_featured", "product_type",
            "average_rating", "product_category", "product_tag",
            "images", "variants", "created_at"
        ]
