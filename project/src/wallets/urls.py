from django.urls import path

from .views import (OperationChargeCreateView, OperationsListView,
                    WalletCreateView, WalletRetrieveView)


urlpatterns = [
    path('', WalletCreateView.as_view(), name='wallet_create'),
    path('<uuid:uuid>/', WalletRetrieveView.as_view(), name='wallet'),
    path(
        '<uuid:uuid>/operations/',
        OperationsListView.as_view(),
        name='operations'
    ),
    path(
        '<uuid:uuid>/operations/charge/',
        OperationChargeCreateView.as_view(),
        name='charge_operation'
    ),
]
