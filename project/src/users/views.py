from rest_framework.generics import CreateAPIView

from .serializers import CustomerSerializer


class CustomerCreateView(CreateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = ()
