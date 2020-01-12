from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import WalletSerializer

from utils.permissions import IsCustomer


class WalletCreateView(CreateAPIView):
    serializer_class = WalletSerializer
    permission_classes = (IsAuthenticated, IsCustomer, )
