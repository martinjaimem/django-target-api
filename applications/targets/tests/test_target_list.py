from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status

from .factories import TargetFactory
from applications.users.tests.factories import UserFactory


class TargetCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('target-list')

    def call_targets_list(self):
        return self.client.get(self.url)

    def setUp(self):
        self.user = UserFactory(confirmed=True)

    def test_no_created_targets_return_empty(self):
        self.client.force_authenticate(user=self.user)
        response = self.call_targets_list()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 0)
        self.assertEqual(len(response.data.get('results')), 0)

    def test_created_targets_return_targets(self):
        targets_count = 10
        TargetFactory.create_batch(size=targets_count, owner=self.user)

        self.client.force_authenticate(user=self.user)
        response = self.call_targets_list()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), targets_count)
        self.assertEqual(len(response.data.get('results')), targets_count)
        self.assertEqual(
            [key for key in response.json()['results'][0]],
            ['id', 'latitude', 'longitude', 'owner', 'radius', 'title', 'topic', ]
        )

    def test_diff_users_created_targets_return_only_user_targets(self):
        targets_count = 10
        user_targets = TargetFactory.create_batch(size=targets_count, owner=self.user)
        other_user = UserFactory(confirmed=True)
        TargetFactory.create_batch(size=targets_count, owner=other_user)

        self.client.force_authenticate(user=self.user)
        response = self.call_targets_list()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), targets_count)
        self.assertEqual(
            [t['id'] for t in response.json()['results']],
            [t.id for t in user_targets]
        )

    def test_no_loged_user_respond_unauthorized(self):
        response = self.call_targets_list()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
