from django.core import mail
import factory
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status

from .factories import BaseUserFactory
from applications.users.models import User


class UserRegistrationTests(APITestCase):
    format = 'json'

    @staticmethod
    def build_params():
        params = factory.build(dict, FACTORY_CLASS=BaseUserFactory)
        params['password1'] = params['password2'] = params['password']
        return params

    def setUp(self):
        self.url = reverse('rest_register')

    def test_all_params_right_respond_success(self):
        params = self.build_params()
        response = self.client.post(self.url, params, format=self.format)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'detail': 'Verification e-mail sent.'})

    def test_all_params_right_send_confirmation_email(self):
        params = self.build_params()
        self.client.post(self.url, params, format=self.format)

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(params['email'], mail.outbox[0].to)

    def test_all_params_right_store_date(self):
        params = self.build_params()
        response = self.client.post(self.url, params, format=self.format)

        last_user = User.objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(last_user.email, params['email'])
        self.assertEqual(last_user.name, params['name'])
        self.assertEqual(last_user.gender, params['gender'])

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
        user = BaseUserFactory()
        params = self.build_params()
        params['email'] = user.email

        response = self.client.post(self.url, params, format=self.format)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'email': ['A user is already registered with this e-mail address.']}
        )
