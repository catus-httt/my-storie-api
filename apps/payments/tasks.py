from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from apps.orders.models import Order, OrderItem


@shared_task
def send_order_confirmation_email(order_id):
    order = Order.objects.prefetch_related("items").get(id=order_id)
    items = order.items.all()

    lines = []
    for item in items:
        label = item.product_title
        if item.variant_name:
           label += f" ({item.variant_name})"
        lines.append(f" -{label} x{item.quantity} {item.total_price} EUR") 

    body = (
        f"Bonjour {order.user.email},\n\n"
        f"Votre commande #{order.id} a été confirmée.\n\n"
        f"Articles :\n" + "\n".join(lines) + f"\n\n"
        f"Total : {order.total_amount} EUR\n"
        f"Adresse de livraison : {order.shipping_address}\n\n"
        f"Merci pour votre achat !\n"
    )

    send_mail(
        subject=f"Confirmation de commande #{order.id}",
        message=body,
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@mystorie.local"),
        recipient_list=[order.user.email],
        fail_silently=True,
    )

    return f"Order confirmation sent for order {order_id}"