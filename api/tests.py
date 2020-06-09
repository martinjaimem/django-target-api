from django.test import TestCase


class ApiTest(TestCase):
    def test_check_if_runs(self):
        self.assertIs(True, True)
