from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.cart.models import Cart, CartItem
from apps.cart.serializers import CartSerializer
from apps.products.models import Product, ProductVariant


def get_checkout_user(request):
    if request.user.is_authenticated:
        return request.user

    user, _ = User.objects.get_or_create(
        email="creator@mystorie.local",
        defaults={"username": "mystorie_creator", "is_staff": True},
    )
    return user


def get_user_cart(request):
    user = get_checkout_user(request)
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


class CartDetailView(APIView):
    def get(self, request):
        cart = get_user_cart(request)
        serializer = CartSerializer(cart, context={"request": request})
        return Response(serializer.data)


class CartAddItemView(APIView):
    def post(self, request):
        cart = get_user_cart(request)
        product_id = request.data.get("product_id")
        variant_id = request.data.get("variant_id")
        quantity = int(request.data.get("quantity", 1))

        if not product_id:
            return Response({"message": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        product = Product.objects.get(id=product_id, is_active=True)
        variant = None

        if variant_id:
            variant = ProductVariant.objects.get(id=variant_id, product=product, is_active=True)
        else:
            variant = product.variants.filter(is_active=True).first()

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={"quantity": quantity},
        )

        if not created:
            item.quantity += quantity
            item.save(update_fields=["quantity"])

        serializer = CartSerializer(cart, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartItemUpdateView(APIView):
    def patch(self, request, item_id):
        cart = get_user_cart(request)
        quantity = int(request.data.get("quantity", 1))
        item = CartItem.objects.get(id=item_id, cart=cart)

        if quantity <= 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save(update_fields=["quantity"])

        serializer = CartSerializer(cart, context={"request": request})
        return Response(serializer.data)

    def delete(self, request, item_id):
        cart = get_user_cart(request)
        CartItem.objects.filter(id=item_id, cart=cart).delete()
        serializer = CartSerializer(cart, context={"request": request})
        return Response(serializer.data)
