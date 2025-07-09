from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import BookingViewSet, PropertyViewSet,InitiatePaymentView, VerifyPaymentView

router = DefaultRouter()
router.register(r'property', PropertyViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = router.urls



urlpatterns += [
    path('initiate-payment/', InitiatePaymentView.as_view()),
    path('verify-payment/', VerifyPaymentView.as_view()),
]
