from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Wallet
from .serializers import WalletSerializer

from utils.permissions import IsCustomer, IsOwner


class WalletCreateView(CreateAPIView):
    serializer_class = WalletSerializer
    permission_classes = (IsAuthenticated, IsCustomer, )


class WalletRetrieveView(RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes = (IsAuthenticated, IsOwner, )
    lookup_field = 'uuid'
    queryset = Wallet.objects.all()
