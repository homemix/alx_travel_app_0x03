import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from faker import Faker

from alx_travel_app.listings.models import Booking, Message, Payment, Property, Review

fake = Faker()


class Command(BaseCommand):
    help = "Seed the database with sample data"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Seeding database..."))

        properties = self.create_properties(10)
        bookings = self.create_bookings(properties, 20)
        self.create_payments(bookings, 20)
        self.create_reviews(properties, 15)
        self.create_messages(10)

        self.stdout.write(self.style.SUCCESS("Seeding completed!"))

    def create_properties(self, count):
        properties = []
        for _ in range(count):
            property = Property.objects.create(
                name=fake.company(),
                description=fake.text(),
                location=fake.city(),
                price_per_night=round(random.uniform(50, 500), 2)
            )
            properties.append(property)
        return properties

    def create_bookings(self, properties, count):
        bookings = []
        for _ in range(count):
            property_obj = random.choice(properties)
            start_date = fake.date_between(start_date='-30d', end_date='today')
            end_date = start_date + timedelta(days=random.randint(1, 10))
            total_price = property_obj.price_per_night * (end_date - start_date).days

            booking = Booking.objects.create(
                property_id=property_obj,
                start_date=start_date,
                end_date=end_date,
                total_price=total_price,
                status=random.choice(['pending', 'confirmed', 'canceled'])
            )
            bookings.append(booking)
        return bookings

    def create_payments(self, bookings, count):
        for _ in range(count):
            booking = random.choice(bookings)
            Payment.objects.create(
                booking_id=booking,
                amount=booking.total_price,
                payment_date=fake.date_between(start_date=booking.start_date),
                payment_method=random.choice(['credit_card', 'paypal', 'stripe'])
            )

    def create_reviews(self, properties, count):
        for _ in range(count):
            Review.objects.create(
                property_id=random.choice(properties),
                rating=random.randint(1, 5)
            )

    def create_messages(self, count):
        for _ in range(count):
            Message.objects.create(
                message_body=fake.paragraph()
            )
