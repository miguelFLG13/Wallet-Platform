import uuid
from polymorphic.models import PolymorphicModel

from django.db import models


class Wallet(PolymorphicModel):
    """
    Wallet definition
    """
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    money = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return str(self.uuid)


class CustomerWallet(Wallet):
    """
    Customer Wallet definition
    """
    customer = models.ForeignKey(
        'users.Customer',
        related_name='wallets',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['customer']
        indexes = [models.Index(fields=['customer'])]


class CommerceWallet(Wallet):
    """
    Commerce Wallet definition
    """
    commerce = models.OneToOneField(
        'users.Commerce',
        related_name='wallets',
        on_delete=models.CASCADE
    )


class Operation(models.Model):
    """
    Wallet Operation definition
    """
    PENDING = '1'
    DONE = '2'
    ERROR = '3'

    OPERATION_STATUS = (
        (PENDING, 'Pending'),
        (DONE, 'Done'),
        (ERROR, 'Error'),
    )

    CHARGE = '1'
    TRANFER = '2'

    OPERATION_TYPES = (
        (CHARGE, 'Charge'),
        (TRANFER, 'Tranfer'),
    )

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    type = models.CharField(
        choices=OPERATION_STATUS,
        max_length=10,
        default=PENDING
    )
    status = models.CharField(
        choices=OPERATION_STATUS,
        max_length=10,
        default=PENDING
    )
    from_wallet = models.ForeignKey(
        'Wallet',
        related_name='from_operations',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    to_wallet = models.ForeignKey(
        'Wallet',
        related_name='to_operations',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['type']
        indexes = [models.Index(fields=['to_wallet', 'from_wallet'])]

    def __str__(self):
        return str(self.uuid)
