import unittest
from unittest import TestCase
from tag_manager.utils_tag_name import *


class TagUtilTestCase(TestCase):
    def setUp(self):
        pass

    def test_tag_name(self):
        self.assertEqual(decode_tag_name("가나다라%23"), "가나다라#")
        self.assertEqual(encode_tag_name("가나다라#"), "가나다라%23")

    def test_tag_name_safe(self):
        self.assertEqual(tag_name_safe("#가나다라#  "), "가나다라#")
        self.assertEqual(tag_name_safe(" $ 가나 다라 ,.. "), "가나-다라")
        self.assertEqual(tag_name_safe("Abc dEf"), "Abc-dEf")
    
    def test_tag_slugify(self):
        self.assertEqual(tag_slugify("Abc dEf"), "abc-def")
        self.assertEqual(tag_slugify("Abc #"), "abc-#")


def tt():
    tag_str = "pYthon, jAva, Oracle"
    # tag_str = ''
    tag_slugs_origin = ['python', 'php']

    # tag_list = {tag_slugify(value):value for value in enumerate(tag_name_list)}
    # print(tag_list)
    # my_dict = {tag_slugify(x): tag_name_safe(x) for x in tag_name_list}
    tag_list = convert_str_to_tags_dict(tag_str)
    print(tag_list)
    slug_list = list(tag_list.keys())
    print(slug_list)

    slugs_to_remove_list = list(set(tag_slugs_origin).difference(set(slug_list))) # origin - slug_list
    print(slugs_to_remove_list)

    # 새로 추가된 태그
    slugs_to_add_list = list(set(slug_list).difference(set(tag_slugs_origin))) # tag_list - origin
    print(slugs_to_add_list)
    
    for tag_slug in slugs_to_add_list:
        if len(tag_slug) > 0:
            print(tag_slug)
            print(tag_list[tag_slug])

if __name__ == '__main__':
    unittest.main()
    # tt()