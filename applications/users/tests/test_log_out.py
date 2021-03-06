from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status

from .factories import UserFactory


class UserLogOutTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('rest_logout')

    def call_log_out(self):
        return self.client.post(self.url)

    def setUp(self):
        self.user = UserFactory(confirmed=True)

    def test_valid_tokenf_respond_success(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = self.call_log_out()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse('rest_user_details'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_token_respond_unauthorized(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token fakeToken')
        response = self.call_log_out()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
