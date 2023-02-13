import unicodedata
import re
from django.utils.text import slugify


def tag_name_encode(value, allow_unicode=False):
    """
    태그명이 저장될 때에 공백이나 특수문자를 제거함.
      - 공백은 '-'로 치환됨
      - 특수문자 중 #은 유지됨.
    참고
      - https://github.com/django/django/blob/main/django/utils/text.py#L420
    """
    if allow_unicode:
        value = str(value)
        value = unicodedata.normalize("NFKC", value)
        value = re.sub(r"[^\w\s\#-]", "", value.lower())
        # 첫 문자가 #인 것은 제거되게 해야할 듯한데.
        value = re.sub(r"^(\#)", "", value)
        value = re.sub(r"[-\s]+", "-", value).strip("-_")
        return value
    else:
        return slugify(value, allow_unicode=False)

def get_tag_code_from_name(value):
    value = str(value)
    return value.replace("#", "%23")

def get_tag_name_from_code(value):
    value = str(value)
    return value.replace("%23", "#")