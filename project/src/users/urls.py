from django.urls import path

from .views import CommerceCreateView, CustomerCreateView


urlpatterns = [
    path('customer/', CustomerCreateView.as_view(), name='customer_create'),
    path('commerce/', CommerceCreateView.as_view(), name='commerce_create'),
]
