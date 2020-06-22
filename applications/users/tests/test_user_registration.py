from django.core import mail
from django.test import TestCase
import factory
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework.views import status

from .factories import UserFactory

class UserRegistrationTests(APITestCase):
    url = '/api/v1/auth/registration/'
    format = 'json'

    @staticmethod
    def build_params():
        params = factory.build(dict, FACTORY_CLASS=UserFactory)
        params['password1'] = params['password2'] = params['password']
        return params


    def test_all_params_right_respond_success(self):
        params = self.build_params()
        response = self.client.post(self.url, params, format=self.format)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, { 'detail': 'Verification e-mail sent.' })

    def test_all_params_right_send_confirmation_email(self):
        params = self.build_params()
        self.client.post(self.url, params, format=self.format)

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(params['email'], mail.outbox[0].to)

    def test_missing_password_respond_failure(self):
        params = self.build_params()
        params['password1'] = ''

        response = self.client.post(self.url, params, format=self.format)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_confirmation_password_respond_failure(self):
        params = self.build_params()
        params['password2'] = ''

        response = self.client.post(self.url, params, format=self.format)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_name_respond_failure(self):
        params = self.build_params()
        del params['name']

        response = self.client.post(self.url, params, format=self.format)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_gender_respond_failure(self):
        params = self.build_params()
        del params['gender']

        response = self.client.post(self.url, params, format=self.format)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_exisiting_email_respond_failure(self):
        user = UserFactory()
        params = self.build_params()
        params['email'] = user.email

        response = self.client.post(self.url, params, format=self.format)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            { 'email': ['A user is already registered with this e-mail address.'] }
        )
