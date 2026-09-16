from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.views import get_checkout_user
from apps.downloads.services import grant_download_access_for_order
from apps.orders.models import Order
from apps.payments.models import Payment
from apps.payments.serializers import PaymentSerializer
from apps.payments.tasks import send_order_confirmation_email


class PaymentCreateView(APIView):
    def post(self, request):
        user = get_checkout_user(request)
        order_id = request.data.get("order_id")

        if not order_id:
            return Response({"message": "order_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.get(id=order_id, user=user)
        payment, _ = Payment.objects.get_or_create(
            order=order,
            defaults={
                "provider": Payment.PROVIDER_STRIPE,
                "amount": order.total_amount,
                "currency": "EUR",
                "provider_payment_id": f"test_order_{order.id}",
                "checkout_url": f"/checkout/success?order_id={order.id}",
            },
        )

        serializer = PaymentSerializer(payment, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PaymentConfirmView(APIView):
    def post(self, request, payment_id):
        user = get_checkout_user(request)
        payment = Payment.objects.select_related("order").get(id=payment_id, order__user=user)
        payment.status = Payment.STATUS_SUCCEDED
        payment.save(update_fields=["status", "updated_at"])

        order = payment.order
        order.status = Order.STATUS_PAID
        order.paid_at = timezone.now()
        order.save(update_fields=["status", "paid_at"])

        grant_download_access_for_order(order)

        send_order_confirmation_email.delay(order.id)

        #serializer = PaymentSerializer(payment, context={"request": request})
        #return Response(serializer.data)

        return Response({
            "message": "Commande payée avec succès",
            "order_id": order.id
        })