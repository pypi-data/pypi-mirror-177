from django.test import TestCase

from django_hawk.tests.test_views import DjangoHawkViewTests


class DjangoViewTests(DjangoHawkViewTests, TestCase):
    view_name = "test_simple_view"
