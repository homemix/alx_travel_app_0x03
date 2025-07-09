from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_payment_confirmation_email(email, booking_id):
    subject = "Booking Confirmed"
    message = f"Your booking with ID {booking_id} has been confirmed. Thank you for your payment!"
    send_mail(subject, message, 'no-reply@travel.com', [email])
