from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status

from .factories import TopicFactory
from applications.users.tests.factories import UserFactory


class UserTopicListTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('target-topic-list')

    def setUp(self):
        self.user = UserFactory(confirmed=True)

    def call_topics_list(self):
        return self.client.get(self.url)

    def test_no_created_topics_return_empty(self):
        self.client.force_authenticate(user=self.user)
        response = self.call_topics_list()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 0)
        self.assertEqual(len(response.data.get('results')), 0)

    def test_created_topics_return_topics(self):
        topics_count = 10
        TopicFactory.create_batch(size=topics_count)

        self.client.force_authenticate(user=self.user)
        response = self.call_topics_list()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), topics_count)
        self.assertEqual(len(response.data.get('results')), topics_count)

    def test_no_loged_user_respond_unauthorized(self):
        response = self.call_topics_list()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
