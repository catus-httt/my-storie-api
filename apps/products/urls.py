from django.urls import path
from apps.products.views import ProductListView, ProductDetailView, ProductSearchView

urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),
    path("search/", ProductSearchView.as_view(), name="product-search"),
    path("<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),
]