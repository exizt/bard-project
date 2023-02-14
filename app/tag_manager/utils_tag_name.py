import unicodedata
import re
from django.utils.text import slugify


def tag_name_safe(value: str):
    """
    태그명이 저장될 때에 공백이나 특수문자를 제거함.
      - 공백은 '-'로 치환됨
      - 특수문자 중 #은 유지됨. (기존 slugify 함수에서 수정한 부분)
    참고
      - https://github.com/django/django/blob/main/django/utils/text.py#L420
    """
    value = value.strip() # 좌우 공백 제거
    value = unicodedata.normalize("NFKC", value) # 문자 분석 후 정규화(애매한 국제 글자 등이 영어로 전환됨)
    # value = value.lower() # 소문자 처리
    value = re.sub(r"[^\w\s\#-]", "", value) # 문자, 공백, -, #을 제외한 글자 제거
    value = re.sub(r"^(\#)", "", value) # 첫글자가 #이 온 경우 # 제거
    value = re.sub(r"[-\s]+", "-", value).strip("-_") # 공백을 -로 치환
    return value

def tag_slugify(value: str):
    # return tag_name_safe(value).replace("#", "%23").lower()
    return tag_name_safe(value).lower()

def convert_str_to_tags_dict(tag_str):
    """
    'tag1, tag2'의 문자열을 {slug: tag_name} 형태의 딕셔너리로 변환
    """
    tag_str = str(tag_str)
    tag_names = tag_str.split(',') if len(tag_str) > 0 else []
    return {tag_slugify(x): tag_name_safe(x) for x in tag_names}

def tag_name_safe_2(value, allow_unicode=False):
    """
    태그명이 저장될 때에 공백이나 특수문자를 제거함.
      - 공백은 '-'로 치환됨
      - 특수문자 중 #은 유지됨. (기존 slugify 함수에서 수정한 부분)
    참고
      - https://github.com/django/django/blob/main/django/utils/text.py#L420
    """
    if allow_unicode:
        value = str(value)
        value = unicodedata.normalize("NFKC", value) # 문자 분석 후 정규화(애매한 국제 글자 등이 영어로 전환됨)
        value = value.lower() # 소문자 처리
        value = re.sub(r"[^\w\s\#-]", "", value) # 문자, 공백, -, #을 제외한 글자 제거
        value = re.sub(r"^(\#)", "", value) # 첫글자가 #이 온 경우 # 제거
        value = re.sub(r"[-\s]+", "-", value).strip("-_") # 공백을 -로 치환
        return value
    else:
        return slugify(value, allow_unicode=False)

def encode_tag_name(value):
    """
    태그명에서 #을 'urlencode'로 변환.
    """
    value = str(value)
    return value.replace("#", "%23")

def decode_tag_name(value):
    """
    url code 값에서 %23 등을 #으로 변환.
    """
    value = str(value)
    return value.replace("%23", "#")
