import uuid
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from ..models import Operation, Wallet

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
    """ Test module for GET a Wallet API """

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

    def test_get_commerce_wallet_valid(self):
        commerce = mommy.make('users.commerce')
        wallet = mommy.make(
            'wallets.commercewallet',
            commerce=commerce,
        )
        url = reverse('wallet', args=[wallet.uuid])
        headers = {"Authorization": "Bearer {}".format(
            generate_test_token(self.application, commerce))}
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(uuid.UUID(response.data['uuid']), wallet.uuid)

    def test_get_wallet_incorrect_user_invalid(self):
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

    def test_get_wallet_incorrect_uuid_invalid(self):
        url = reverse('wallet', args=[uuid.uuid4()])
        customer = mommy.make('users.customer')
        mommy.make('wallets.customerwallet', customer=customer)
        headers = {"Authorization": "Bearer {}".format(
            generate_test_token(self.application, customer))}
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GetOperationsTest(APITestCase):
    """ Test module for GET Operations API """

    def setUp(self):
        self.application = generate_test_application()
        self.total_correct_operations = 2
        self.customer = mommy.make('users.customer')

    def test_get_operations_valid(self):
        wallet = mommy.make(
            'wallets.customerwallet',
            customer=self.customer,
        )
        operation_from = mommy.make('wallets.operation', from_wallet=wallet)
        operation_to = mommy.make('wallets.operation', to_wallet=wallet)
        mommy.make('wallets.operation')
        url = reverse('operations', args=[wallet.uuid])
        headers = {"Authorization": "Bearer {}".format(
            generate_test_token(self.application, self.customer))}
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.total_correct_operations)
        self.assertEqual(
            uuid.UUID(response.data[0]['uuid']),
            operation_from.uuid
        )
        self.assertEqual(
            uuid.UUID(response.data[1]['uuid']),
            operation_to.uuid
        )

    def test_get_wallet_incorrect_user_invalid(self):
        wallet = mommy.make(
            'wallets.customerwallet',
            customer=mommy.make('users.customer'),
        )
        url = reverse('operations', args=[wallet.uuid])
        mommy.make(
            'wallets.operation',
            from_wallet=mommy.make('wallets.customerwallet', customer=self.customer)
        )
        headers = {"Authorization": "Bearer {}".format(
            generate_test_token(self.application, self.customer))}
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
 
    def test_get_wallet_incorrect_uuid_invalid(self):
        url = reverse('wallet', args=[uuid.uuid4()])
        mommy.make('wallets.customerwallet', customer=self.customer)
        headers = {"Authorization": "Bearer {}".format(
            generate_test_token(self.application, self.customer))}
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostChargeOperationTest(APITestCase):
    """ Test module for POST a Charge Operation API """

    def setUp(self):
        self.start_money = 3
        self.customer = mommy.make('users.customer')
        self.wallet = mommy.make(
            'wallets.customerwallet',
            money=self.start_money,
            customer=self.customer
        )
        self.url = reverse('charge_operation', args=[self.wallet.uuid])
        self.application = generate_test_application()
        self.headers = {"Authorization": "Bearer {}".format(
            generate_test_token(self.application, self.customer))}

    def test_charge_operation_valid(self):
        charge_money = 3
        payload = {'money': charge_money}
        response = self.client.post(self.url, payload, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        operation = Operation.objects.order_by('id').last()
        self.assertEqual(operation.to_wallet, self.wallet)
        self.assertEqual(operation.money, charge_money)
        self.assertEqual(operation.type, Operation.CHARGE)
        self.assertEqual(operation.status, Operation.DONE)
        self.assertEqual(operation.to_wallet.money, self.start_money + charge_money)

    def test_charge_operation_not_autheticate_user_invalid(self):
        charge_money = 3
        payload = {'money': charge_money}
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_charge_operation_incorrect_wallet_invalid(self):
        url = reverse('charge_operation', args=[uuid.uuid4()])
        charge_money = 3
        payload = {'money': charge_money}
        response = self.client.post(url, payload, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_charge_operation_money_gretater_than_limit_invalid(self):
        charge_money = 10000
        payload = {'money': charge_money}
        response = self.client.post(self.url, payload, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_charge_operation_sum_money_gretater_than_limit_invalid(self):
        charge_money = 9997
        payload = {'money': charge_money}
        response = self.client.post(self.url, payload, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_charge_operation_incorrect_negative_money_invalid(self):
        charge_money = -3
        payload = {'money': charge_money}
        response = self.client.post(self.url, payload, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
