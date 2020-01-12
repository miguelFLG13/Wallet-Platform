from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Q

from .models import Operation, Wallet


def get_operations_by_wallet_uuid(uuid):
    """
    Get operations of a wallet

    :param uuid: uuid of a wallet
    :type uuid: UUID
    :return: Operations of the wallet
    :return type: PolymorphicQuerySet
    """
    return Operation.objects.filter(
        Q(from_wallet__uuid=uuid)|Q(to_wallet__uuid=uuid)
    )
