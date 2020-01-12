import uuid
from decimal import Decimal
from polymorphic.models import PolymorphicModel

from django.core.validators import MinValueValidator
from django.db import models

from .exceptions import ApplyChargeException


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
        default=0,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    def __str__(self):
        return str(self.uuid)

    def apply_operation(self, money):
        self.money += money
        self.save()


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
        related_name='wallet',
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
    money = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    class Meta:
        ordering = ['type']
        indexes = [models.Index(fields=['to_wallet', 'from_wallet'])]

    def __str__(self):
        return str(self.uuid)

    def apply(self):
        if self.status != self.DONE:
            try:
                if self.to_wallet:
                    self.to_wallet.apply_operation(self.money)

                if self.from_wallet:
                    self.from_wallet.apply_operation(self.money*-1)
                self.status = self.DONE
                self.save()
            except Exception:
                self.status = self.ERROR
                raise ApplyChargeException("Incorrect Operation")
