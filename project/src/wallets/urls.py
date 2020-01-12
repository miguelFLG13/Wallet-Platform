from django.urls import path

from .views import WalletCreateView, WalletRetrieveView


urlpatterns = [
    path('', WalletCreateView.as_view(), name='wallet_create'),
    path('<uuid:uuid>/', WalletRetrieveView.as_view(), name='wallet'),
]
