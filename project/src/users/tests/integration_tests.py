import uuid
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from ..models import Customer


class PostCustomerTest(APITestCase):
    """ Test module for POST a Customer API """

    def setUp(self):
        self.url = reverse('customer_create')

    def test_post_customer_valid(self):
        customer_data = {
            'first_name': 'Miguel',
            'last_name': 'Perez Lopez',
            'personal_id': '36782930T',
            'username': 'mpl123',
            'password': '123456',
            'email': 'miguel.perez@gmail.com',
            'phone': '654637829'
        }
        response = self.client.post(self.url, customer_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        customer = Customer.objects.order_by('id').last()
        self.assertEqual(uuid.UUID(response.data['uuid']), customer.uuid)
