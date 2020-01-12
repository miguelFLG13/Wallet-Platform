import uuid
from polymorphic.models import PolymorphicModel

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(PolymorphicModel, AbstractUser):
    """
    User definition
    """
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    phone = models.CharField(max_length=15)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return self.username

    def is_customer(self):
        """
        Check if a user is a customer

        :return: if is a customer
        :return type: bool
        """
        if self.polymorphic_ctype.model == 'customer':
            return True
        return False

    def is_commerce(self):
        """
        Check if a user is a commerce

        :return: if is a commerce
        :return type: bool
        """
        if self.polymorphic_ctype.model == 'commerce':
            return True
        return False


class Customer(User):
    """
    Customer definition
    """
    personal_id = models.CharField(max_length=10)


class Commerce(User):
    """
    Commerce definition
    """
    corporate_name = models.CharField(max_length=10)
    cif = models.CharField(max_length=10)
