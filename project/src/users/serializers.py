from rest_framework.serializers import ModelSerializer

from .models import Customer


class CustomerSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = ('uuid', 'first_name', 'last_name', 'personal_id', 'username',
                  'password', 'email', 'phone', )
        read_only_fields = ('uuid', )
        extra_kwargs = {
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'personal_id': {'write_only': True},
            'username': {'write_only': True},
            'password': {'write_only': True},
            'email': {'write_only': True},
            'phone': {'write_only': True},
        }
