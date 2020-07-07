from django.contrib.sites.models import Site
from django.core import mail
from django.test import TestCase
import factory
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework.views import status
from faker import Factory, Faker

from .factories import UserFactory
from applications.users.models import User


class ConfirmedUserLogInTests(APITestCase):
    url = reverse('rest_login')
    fake = Faker()

    def call_log_in(self):
        return self.client.post(self.url, self.params)

    def setUp(self):
        self.password = self.fake.password(length=8)
        self.user = UserFactory(password=self.password, confirmed=True)
        self.params = { 'email': self.user.email, 'password': self.password }

    def test_all_params_right_respond_success(self):
        response = self.call_log_in()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('key'))

    def test_missing_email_responds_failure(self):
        del self.params['email']
        response = self.call_log_in()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_password_responds_failure(self):
        del self.params['password']
        response = self.call_log_in()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_password_responds_failure(self):
        self.params['password'] = self.fake.password(length=8)
        response = self.call_log_in()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UnconfirmedUserLogInTests(APITestCase):
    url = reverse('rest_login')
    fake = Faker()

    def call_log_in(self):
        return self.client.post(self.url, self.params)

    def setUp(self):
        self.password = self.fake.password(length=8)
        self.user = UserFactory(password=self.password)
        self.params = { 'email': self.user.email, 'password': self.password }

    def test_all_params_right_responds_unconfirmed_email(self):
        response = self.call_log_in()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            { 'non_field_errors': ['E-mail is not verified.'] }
        )
