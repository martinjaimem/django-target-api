from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status

from .factories import TargetFactory
from applications.users.tests.factories import UserFactory
from applications.targets.models import Target


class TargetDeleteTest(APITestCase):
    def call_targets_delete(self, pk):
        url = reverse('target-detail', args=(pk,))
        return self.client.delete(url)

    def setUp(self):
        self.user = UserFactory(confirmed=True)

    def test_no_created_targets_responds_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.call_targets_delete(1)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_created_targets_responds_success(self):
        targets_count = 10
        targets = TargetFactory.create_batch(size=targets_count, owner=self.user)

        self.client.force_authenticate(user=self.user)
        response = self.call_targets_delete(targets[0].id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            Target.objects.filter(owner=self.user).count(),
            targets_count - 1
        )

    def test_diff_user_created_targets_responds_failure(self):
        targets_count = 10
        TargetFactory.create_batch(size=targets_count, owner=self.user)
        other_user = UserFactory(confirmed=True)
        other_targets = TargetFactory.create_batch(size=targets_count, owner=other_user)

        self.client.force_authenticate(user=self.user)
        response = self.call_targets_delete(other_targets[0].id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            Target.objects.filter(owner=self.user).count(),
            targets_count
        )
        self.assertEqual(
            Target.objects.filter(owner=other_user).count(),
            targets_count
        )

    def test_no_loged_user_respond_unauthorized(self):
        response = self.call_targets_delete(1)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
