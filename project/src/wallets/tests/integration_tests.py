import uuid
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from ..models import Wallet

from utils.test_services import generate_test_application, generate_test_token


class PostWalletTest(APITestCase):
    """ Test module for POST a Wallet API """

    def setUp(self):
        self.url = reverse('wallet_create')
        self.application = generate_test_application()

    def test_post_wallet_valid(self):
        headers = {"Authorization": "Bearer {}".format(
            generate_test_token(self.application, mommy.make('users.customer')))}
        response = self.client.post(self.url, **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        wallet = Wallet.objects.order_by('id').last()
        self.assertEqual(uuid.UUID(response.data['uuid']), wallet.uuid)

    def test_post_wallet_incorrect_user_invalid(self):
        headers = {"Authorization": "Bearer {}".format(
            generate_test_token(self.application, mommy.make('users.commerce')))}
        response = self.client.post(self.url, **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GetWalletTest(APITestCase):
    """ Test module for POST a Wallet API """

    def setUp(self):
        self.application = generate_test_application()

    def test_get_customer_wallet_valid(self):
        customer = mommy.make('users.customer')
        wallet = mommy.make(
            'wallets.customerwallet',
            customer=customer,
        )
        url = reverse('wallet', args=[wallet.uuid])
        headers = {"Authorization": "Bearer {}".format(
            generate_test_token(self.application, customer))}
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(uuid.UUID(response.data['uuid']), wallet.uuid)

    def test_get_customer_wallet_incorrect_user_invalid(self):
        wallet = mommy.make(
            'wallets.customerwallet',
            customer=mommy.make('users.customer'),
        )
        url = reverse('wallet', args=[wallet.uuid])
        customer = mommy.make('users.customer')
        mommy.make('wallets.customerwallet', customer=customer)
        headers = {"Authorization": "Bearer {}".format(
            generate_test_token(self.application, mommy.make('users.customer')))}
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_customer_wallet_incorrect_uuid_invalid(self):
        url = reverse('wallet', args=[uuid.uuid4()])
        customer = mommy.make('users.customer')
        mommy.make('wallets.customerwallet', customer=customer)
        headers = {"Authorization": "Bearer {}".format(
            generate_test_token(self.application, customer))}
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
