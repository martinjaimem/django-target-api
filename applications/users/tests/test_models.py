from django.test import TestCase

from applications.users.models import User
from .factories import UserFactory


class UserModelTests(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_to_string_displays_name(self):
        self.assertEqual(self.user.name, str(self.user))
