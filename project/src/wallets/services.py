from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from django.db.models import Q

from .errors import APPLY_CHARGE_ERROR
from .exceptions import ApplyChargeException
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
        Q(from_wallet__uuid=uuid) | Q(to_wallet__uuid=uuid)
    )


@transaction.atomic()
def apply_charge(money, wallet_uuid):
    """
    Create and apply a charge in a wallet

    :param money: money of the charge
    :type money: Decimal
    :param wallet_uuid: uuid of a wallet
    :type wallet_uuid: UUID
    :return: error if be error
    :return type: str or None
    """
    try:
        wallet = Wallet.objects.get(uuid=wallet_uuid)
    except ObjectDoesNotExist:
        return APPLY_CHARGE_ERROR[0]

    money = Decimal(money)
    if money < 0:
        return APPLY_CHARGE_ERROR[1]

    operation = Operation(
        type=Operation.CHARGE,
        status=Operation.PENDING,
        to_wallet=wallet,
        money=money
    )
    try:
        operation.save()
    except Exception:
        return APPLY_CHARGE_ERROR[1]

    try:
        operation.apply()
    except ApplyChargeException:
        return APPLY_CHARGE_ERROR[2]

    if operation.status != Operation.DONE:
        return APPLY_CHARGE_ERROR[3]
