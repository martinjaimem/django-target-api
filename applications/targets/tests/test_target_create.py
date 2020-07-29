import factory
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status

from .factories import TargetFactory, TopicFactory
from applications.users.tests.factories import UserFactory
from applications.targets.models import Target


class TargetCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('target-list')

    def setUp(self):
        self.user = UserFactory(confirmed=True)
        self.topic = TopicFactory()
        self.params = factory.build(
            dict,
            FACTORY_CLASS=TargetFactory,
            owner=None,
            topic=self.topic.id,
        )

    def call_create_target(self):
        return self.client.post(self.url, self.params)

    def test_all_params_right_respond_success_and_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.call_create_target()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            [key for key in response.json()],
            ['id', 'latitude', 'longitude', 'owner', 'radius', 'title', 'topic', ]
        )

    def test_all_params_right_save_data(self):
        self.client.force_authenticate(user=self.user)
        self.call_create_target()

        last = Target.objects.last()
        self.assertEqual(self.params['latitude'], last.location.x)
        self.assertEqual(self.params['longitude'], last.location.y)
        self.assertEqual(self.user, last.owner)
        self.assertEqual(self.params['radius'], last.radius)
        self.assertEqual(self.params['title'], last.title)
        self.assertEqual(self.topic, last.topic)

    def test_missing_latitude_respond_failure(self):
        del self.params['latitude']

        self.client.force_authenticate(user=self.user)
        response = self.call_create_target()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_longitude_respond_failure(self):
        del self.params['longitude']

        self.client.force_authenticate(user=self.user)
        response = self.call_create_target()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_radius_respond_failure(self):
        del self.params['radius']

        self.client.force_authenticate(user=self.user)
        response = self.call_create_target()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_title_respond_failure(self):
        del self.params['title']

        self.client.force_authenticate(user=self.user)
        response = self.call_create_target()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_topic_respond_failure(self):
        del self.params['topic']

        self.client.force_authenticate(user=self.user)
        response = self.call_create_target()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_loged_user_respond_unauthorized(self):
        response = self.call_create_target()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_created_targets_max_amount_responds_failure(self):
        targets_count = Target.MAX_COUNT_TARGETS_PER_USER
        TargetFactory.create_batch(size=targets_count, owner=self.user)

        self.client.force_authenticate(user=self.user)
        response = self.call_create_target()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Maximum number of targets exceeded']}
        )
        self.assertEqual(
            Target.objects.filter(owner=self.user).count(),
            targets_count
        )

    def test_created_targets_lower_max_amount_responds_success(self):
        targets_count = Target.MAX_COUNT_TARGETS_PER_USER - 1
        TargetFactory.create_batch(size=targets_count, owner=self.user)

        self.client.force_authenticate(user=self.user)
        response = self.call_create_target()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Target.objects.filter(owner=self.user).count(),
            targets_count + 1
        )
