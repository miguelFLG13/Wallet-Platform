from django.urls import path

from .views import OperationsListView, WalletCreateView, WalletRetrieveView


urlpatterns = [
    path('', WalletCreateView.as_view(), name='wallet_create'),
    path('<uuid:uuid>/', WalletRetrieveView.as_view(), name='wallet'),
    path(
        '<uuid:uuid>/operations/',
        OperationsListView.as_view(),
        name='operations'
    ),
]
