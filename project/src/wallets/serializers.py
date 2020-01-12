from rest_framework.serializers import ModelSerializer

from .models import Wallet


class WalletSerializer(ModelSerializer):

    class Meta:
        model = Wallet
        fields = ('uuid', 'money', )
        read_only_fields = ('uuid', )
