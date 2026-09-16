from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from apps.products.models import Product
from apps.products.serializers import ProductSerializer

from apps.products.search import ProductDocument


class ProductSearchView(APIView):
    def get(self, request):
        query = request.query_params.get("q", "")

        search = ProductDocument.search().query(
            "multi_match",
            query=query,
            fields=["title", "description", "product_category.name", "product_tag.name"],
            fuzziness="AUTO",
        )

        results = search[:20].execute()

        data = [
            {
                "id": hit.id,
                "title": hit.title,
                "slug": hit.slug,
                "description": hit.description,
                "base_price": hit.base_price,
                "product_type": hit.product_type,
            }
            for hit in results
        ]

        return Response(data)

class ProductListView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return (Product.objects.filter(is_active=True).select_related("product_category").prefetch_related("product_tag", "images", "variants").order_by("-is_featured", "created_at"))
     

class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Product.objects.filter(is_active=True)