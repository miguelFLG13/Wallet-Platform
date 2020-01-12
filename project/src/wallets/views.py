from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Wallet
from .serializers import OperationSerializer, WalletSerializer
from .services import get_operations_by_wallet_uuid

from utils.permissions import IsCustomer, IsOwner


class WalletCreateView(CreateAPIView):
    serializer_class = WalletSerializer
    permission_classes = (IsAuthenticated, IsCustomer, )


class WalletRetrieveView(RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes = (IsAuthenticated, IsOwner, )
    lookup_field = 'uuid'
    queryset = Wallet.objects.all()


class OperationsListView(ListAPIView):
    serializer_class = OperationSerializer
    permission_classes = (IsAuthenticated, IsOwner, )

    def get_queryset(self, *args, **kwargs):
        return get_operations_by_wallet_uuid(self.kwargs.get('uuid'))
