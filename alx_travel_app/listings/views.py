import requests
from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, Payment, Property
from .serializers import BookingSerializer, PropertySerializer


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class InitiatePaymentView(APIView):
    def post(self, request, *args, **kwargs):
        booking_id = request.data.get("booking_id")
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)

        url = "https://api.chapa.co/v1/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "amount": str(booking.price),
            "currency": "ETB",
            "email": booking.user.email,
            "first_name": booking.user.first_name,
            "last_name": booking.user.last_name,
            "tx_ref": f"TRX-{booking.id}",
            "callback_url": "https://yourdomain.com/api/verify-payment/",
            "return_url": "https://yourdomain.com/payment-complete/",
        }

        response = requests.post(url, headers=headers, json=data)
        res_data = response.json()

        if res_data.get("status") == "success":
            Payment.objects.create(
                booking_id=booking,
                amount=booking.price,
                transaction_id=res_data["data"]["tx_ref"],
            )
            return Response({"checkout_url": res_data["data"]["checkout_url"]})
        else:
            return Response(res_data, status=400)


class VerifyPaymentView(APIView):
    def get(self, request, *args, **kwargs):
        tx_ref = request.GET.get("tx_ref")

        url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"
        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
        }

        response = requests.get(url, headers=headers)
        res_data = response.json()

        try:
            payment = Payment.objects.get(transaction_id=tx_ref)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        if res_data.get("status") == "success" and res_data["data"]["status"] == "success":
            payment.status = "Completed"
            payment.save()
            # Trigger confirmation email via Celery (next step)
            return Response({"message": "Payment verified successfully."})
        else:
            payment.status = "Failed"
            payment.save()
            return Response({"message": "Payment failed or not verified."})

