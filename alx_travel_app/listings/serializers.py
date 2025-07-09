from rest_framework import serializers

from .models import Booking, Property


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['name','description','location','price_per_night']


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ['start_date','end_date','total_price','status']