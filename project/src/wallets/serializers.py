from rest_framework.serializers import ModelSerializer, ValidationError

from .models import Operation, Wallet


class WalletSerializer(ModelSerializer):

    class Meta:
        model = Wallet
        fields = ('uuid', 'money', )
        read_only_fields = ('uuid', )


class OperationSerializer(ModelSerializer):

    class Meta:
        model = Operation
        fields = ('uuid', 'type', 'status', 'from_wallet',
                  'to_wallet', 'money', )
        read_only_fields = ('uuid', 'type', 'status', 'from_wallet',
                            'to_wallet', )

    def validate_money(self, value):
        """
        Check if money is correct
        """
        if value < 0 or value >= 10000:
            raise ValidationError("Incorrect Money")
        return value
