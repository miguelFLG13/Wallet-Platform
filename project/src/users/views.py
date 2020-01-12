from rest_framework.generics import CreateAPIView

from .serializers import CommerceSerializer, CustomerSerializer


class CustomerCreateView(CreateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = ()


class CommerceCreateView(CreateAPIView):
    serializer_class = CommerceSerializer
    permission_classes = ()
