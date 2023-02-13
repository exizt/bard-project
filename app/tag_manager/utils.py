from .models import *
from blog.models import *
from django.utils.text import slugify


def get_tags_by_article(article:Article):
    return article.tags
    # return TagArticle.objects.filter(article_id=article_id)

def get_tag_names_list_by_article(article:Article) -> list:
    """
    해당하는 태그 목록을 조회하여 tag_name을 
    list 타입으로 반환하는 함수
    """
    tags_obj = get_tags_by_article(article)
    tags = tags_obj.values_list('name', flat=True) # flat=true이면 리스트, false이면 튜플 형태로 반환
    return tags

def get_tags_str_by_article(article:Article) -> str:
    """
    해당하는 태그 목록을 조회하여 tag_name을 
    'tag1, tag2'의 문자열 형태로 반환하는 함수
    """
    tag_names_list = get_tag_names_list_by_article(article)

    if len(tag_names_list) > 0:
        return ', '.join(tag_names_list)
    else:
        return None

def save_tags_by_str(article:Article, tag_str):
    """
    'tag1, tag2'의 문자열을 토대로 해당하는 태그를 변경.
    없어진 항목은 delete, 추가된 항목은 insert 처리한다.
    """
    tag_names_origin = get_tag_names_list_by_article(article)

    tag_list = tag_str.split(',') if len(tag_str) > 0 else []
    tag_list = [x.strip() for x in tag_list] # 좌우 공백 제거
    tag_list = [slugify(x, allow_unicode=True) for x in tag_list] # slug 타입으로 변경 (중간의 공백 _ 처리 및 소문자화)

    remove_list = list(set(tag_names_origin).difference(set(tag_list))) # origin - tag_list
    new_list = list(set(tag_list).difference(set(tag_names_origin))) # tag_list - origin


    # 기존에 있다가 제외된 태그 항목을 삭제
    for tag_name in remove_list:
        # TagArticle.objects.filter(article_id=article.id, )
        # Tag.objects.filter(name=tag_name)
        TagArticle.objects.filter(tag__name=tag_name, article_id=article.id).delete()
        # 태그의 카운트 변경이 필요.
        # tag = Tag.objects.filter(name=tag_name).first()
        # Tag.objects.filter(name=tag_name).update(count=F('count')+1)
        tag = Tag.objects.filter(name=tag_name).first()
        if tag.count > 1:
            tag.count -= 1
            tag.save()


    # 추가된 태그 항목에 대해서 생성하거나 변경
    for tag_name in new_list:
        if len(tag_name) > 0:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_article = TagArticle(tag=tag, article_id=article.id)
            tag_article.save()
            # 태그의 카운트 변경이 필요.
            tag.count += 1
            tag.save()
