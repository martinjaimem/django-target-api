from django.test import TestCase

from .factories import TargetFactory, TopicFactory


class TopicModelTests(TestCase):
    def setUp(self):
        self.topic = TopicFactory()

    def test_to_string_displays_name(self):
        self.assertEqual(self.topic.name, str(self.topic))


class TargetModelTests(TestCase):
    def setUp(self):
        self.target = TargetFactory()

    def test_to_string_displays_title(self):
        self.assertEqual(self.target.title, str(self.target))
