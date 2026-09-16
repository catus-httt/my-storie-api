from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from apps.products.models import Product


@registry.register_document
class ProductDocument(Document):
    product_category = fields.ObjectField(
        properties={
            "name": fields.TextField(),
            "slug": fields.KeywordField(),
        }
    )

    product_tag = fields.ObjectField(
        properties={
            "name": fields.TextField(),
            "slug": fields.KeywordField(),
        }
    )

    class Index:
        name = "products"

    class Django:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "product_type",
            "base_price",
            "is_active",
            "is_featured",
            "average_rating",
            "created_at",
        ]

        related_models = []