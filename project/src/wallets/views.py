from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Operation, Wallet
from .serializers import OperationSerializer, WalletSerializer
from .services import apply_charge, get_operations_by_wallet_uuid

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


class OperationChargeCreateView(CreateAPIView):
    serializer_class = OperationSerializer
    permission_classes = (IsAuthenticated, )

    def create(self, request, uuid):
        error = apply_charge(request.POST.get('money', 0), uuid)
        if error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)
