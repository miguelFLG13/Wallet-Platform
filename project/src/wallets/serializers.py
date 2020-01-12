from rest_framework.serializers import ModelSerializer

from .models import Operation, Wallet


class WalletSerializer(ModelSerializer):

    class Meta:
        model = Wallet
        fields = ('uuid', 'money', )
        read_only_fields = ('uuid', )


class OperationSerializer(ModelSerializer):

    class Meta:
        model = Operation
        fields = ('uuid', 'uuid', 'type', 'status', 'from_wallet',
                  'to_wallet')
        read_only_fields = ('__all__', )
