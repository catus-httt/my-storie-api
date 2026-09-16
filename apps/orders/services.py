from django.db import transaction
from apps.orders import Order, OrderItem, OrderStatusHistory

@transaction.atomic
def create_order_from_cart(user, cart, coupon=None):
    subtotal = cart.total_amount
    discount_amount = 0

    if coupon:
        if not coupon.is_valid():
            raise ValueError("Coupon is not valid")
        
        if subtotal < coupon.min_order_amount:
            raise ValueError("Order amount is below coupon minimum")
        
        if coupon.discount_type == "percent": 
            discount_amount = coupon.discount_value * subtotal / 100
        else:
            discount_amount = coupon.discount_value
    
    total_amount = max(subtotal - discount_amount, 0)
    
    order = Order.objects.create(
        user=user,
        subtotal=subtotal,
        discount_amount = discount_amount,
        total_amount = total_amount,
        billing_address = getattr(user.customer_profile, "billing_address", ""),
        shipping_address = getattr(user.customer_profile, "shipping_address", ""),
    )

    for cart_item in cart.items.select_related("product", "variant"):
        product = cart_item.product
        variant = cart_item.variant
        unit_price = cart_item.unit_price

        is_digital = product.product_type in ["digital", "both"]
        is_physical = product.product_type in ["physical", "both"]

        OrderItem.objects.create(
            order=order,
            product=product,
            variant=variant,
            product_title=product.title,
            variant_name=variant.name if variant else "",
            quantity=cart_item.quantity,
            unit_price=unit_price,
            total_price=unit_price * cart_item.quantity,
            is_digital=is_digital,
            is_physical=is_physical,
        )
        
        OrderStatusHistory.objects.create(
            order=order,
            old_status="",
            new_status=Order.STATUS_PENDING,
            note="Order created",
        )

    cart.items.all().delete()

    return order
