from datetime import timedelta
from oauth2_provider.models import get_application_model, AccessToken
from random import randint

from django.db.utils import IntegrityError
from django.utils import timezone


def generate_test_application():
    """
    Generate a outh2 application to create tokens for testing
    """
    Application = get_application_model()
    Application.objects.create(
        name="Test Application",
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_PASSWORD,
    )


def generate_test_token(application, user):
    """
    Get a token of a customer for testing

    :param application: application for generating the token
    :type application: Application
    :param customer: customer to generate the token
    :type customer: Customer
    :return: the customer token
    :return type: str
    """
    while True:
        token = AccessToken(
            user=user,
            scope='read write',
            application=application,
            token=str(randint(0, 999999999)),
            expires=timezone.now() + timedelta(days=1)
        )

        try:
            token.save()
            break
        except IntegrityError:
            pass

    return token.token
