from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

@shared_task
def send_payment_confirmation_email(email, booking_id):
    subject = "Booking Confirmed"
    message = f"Your booking with ID {booking_id} has been confirmed. Thank you for your payment!"
    send_mail(subject, message, 'no-reply@travel.com', [email])

@shared_task
def send_booking_email(recipient_email, customer_name, booking_details):
    subject = 'Booking Confirmation'
    message = f"Dear {customer_name},\n\nYour booking was successful:\n{booking_details}\n\nThank you for using our service!"
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [recipient_email])