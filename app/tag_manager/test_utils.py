from django.test import TestCase
from .utils import *


class TagUtilTestCase(TestCase):
    def setUp(self):
        pass

    def test_tag_name(self):
        self.assertEqual(url_to_tag_name("가나다라%23"), "가나다라#")