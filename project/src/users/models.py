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
