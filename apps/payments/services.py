import stripe
from django.conf import settings
from django.utils import timezone
from apps.orders.models import Order, OrderStatusHistory
from apps.downloads.services import grant_download_access_for_order

from apps.payments.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_checkout_session(order):
    payment, _ = Payment.objects.get_or_create(
        order=order,
        defaults={
            "provider": Payment.PROVIDER_STRIPE,
            "amount": order.total_amount,
            "currency": "EUR",
        },
    )
    
    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        # thứ tự các trường bên trong line_items không quan trọng, nhưng tên các trường và cấu trúc lồng nhau phải đúng
        line_items=[ # danh sách các mục sẽ xuất hiện trên trang thanh toán
            {
                "price_data": { # thông tin giá của một item
                    "currency": payment.currency.lower(),
                    "product_data": { # tên hiển thị trên trang Checkout
                        "name": f"Order #{order.id}",
                    },
                    "unit_amount": int(order.total_amount * 100),
                },
                "quantity": 1,
            }
        ],
        success_url=f"{settings.FRONTEND_URL}/checkout/success?order_id={order.id}", # son rôle est uniquement d'afficher une confirmation à l'utilisateur
        cancel_url=f"{settings.FRONTEND_URL}/checkout/cancel?order_id={order.id}",
        # lors de la création de la sesssion, Stripe stocke les infos de metadata avec la session
        # metadata il sert de lien entre Stripe et la base de données
        metadata={
            "order_id": str(order.id),
            "payment_id": str(payment.id),
        },
    )

    payment.provider_payment_id = session.id
    payment.checkout_url = session.url
    payment.save(update_fields=["provider_payment_id", "checkout_url", "updated_at"])

    return payment

# le webhook recevra un objet ressemblant à ceci:
""" session = {
    "id": "cs_test_xxx",
    "payment_status": "paid",
    "metadata": {
        "order_id": "152",
        "payment_id": "37",
    }
} """


def handle_payment_succeeded(event):
    session = event["data"]["object"]
    order_id = session["metadata"]["order_id"]
    payment_id = session["metadata"]["payment_id"]

    payment = Payment.objects.select_related("order").get(id=payment_id)
    order = payment.order

    payment.status = Payment.STATUS_SUCCEDED
    payment.save(update_fields=["status", "updated_at"])

    old_status = order.status
    order.status = Order.STATUS_PAID
    order.paid_at = timezone.now()
    order.save(update_fields=["status", "paid_at"])

    OrderStatusHistory.objects.create(
        order=order,
        old_status=old_status,
        new_status=Order.STATUS_PAID,
        note="Payment succeeded",
    )

    grant_download_access_for_order(order)