from .models import *
from .utils_tag_name import *
from blog.models import *
from django.utils.text import slugify


def get_tags_by_article(article:Article):
    return article.tags
    # return TagArticle.objects.filter(article_id=article_id)

def get_tag_slugs_list_by_article(article: Article) -> list:
    """
    특정 게시글에 해당되는 태그 목록을 조회하여 태그의 slug를 
    list 타입으로 반환하는 함수
    """
    tags = get_tags_by_article(article)
    return tags.values_list('slug', flat=True) # flat=true이면 리스트, false이면 튜플 형태로 반환

def get_tag_names_list_by_article(article:Article) -> list:
    """
    해당하는 태그 목록을 조회하여 'tag_name'을 
    list 타입으로 반환하는 함수
    @deprecated
    """
    tags = get_tags_by_article(article)
    tag_names = tags.values_list('name', flat=True) # flat=true이면 리스트, false이면 튜플 형태로 반환
    return tag_names

def get_tag_names_str_by_article(article:Article) -> str:
    """
    해당하는 태그 목록을 조회하여 'tag_name'을
    'tag1, tag2'의 문자열 형태로 반환하는 함수
    """
    tag_names = get_tag_names_list_by_article(article)

    if len(tag_names) > 0:
        return ', '.join(tag_names)
    else:
        return None

def save_tags_by_str(article:Article, tag_str):
    """
    'tag1, tag2'의 문자열을 토대로 해당하는 태그를 변경.
    없어진 항목은 delete, 추가된 항목은 insert 처리한다.
    """
    # 기존에 등록된 태그 목록을 조회.
    # tag_names_origin = get_tag_names_list_by_article(article)
    tag_slugs_origin = get_tag_slugs_list_by_article(article)

    # 입력된 태그 문자열(예: 'tag1, tag2')를 변환.
    # tag_str = str(tag_str)
    # tag_name_list = tag_str.split(',') if len(tag_str) > 0 else []
    # tag_list = [x.strip() for x in tag_list] # 좌우 공백 제거
    # tag_list = [slugify(x, allow_unicode=True) for x in tag_list] # slug 타입으로 변경 (중간의 공백 _ 처리 및 소문자화)
    # tag_name_list = [tag_name_safe(x) for x in tag_name_list] # 안전한 명칭으로 변경 (중간의 공백을 '-'로 처리 등)
    # slug_list = [tag_slugify(x) for x in tag_name_list] # slug의 목록을 생성

    # tag_list = {k:v for value in enumerate(tag_name_list)}
    tag_list = convert_str_to_tags_dict(tag_str)
    slug_list = list(tag_list.keys())

    # 기존에는 있었고, 제거될 예정의 태그
    slugs_to_remove_list = list(set(tag_slugs_origin).difference(set(slug_list))) # origin - slug_list

    # 새로 추가된 태그
    slugs_to_add_list = list(set(slug_list).difference(set(tag_slugs_origin))) # tag_list - origin

    # 기존에 있다가 제외된 태그 항목을 삭제
    for tag_slug in slugs_to_remove_list:
        # TagArticle.objects.filter(article_id=article.id, )
        # Tag.objects.filter(name=tag_name)
        TagArticle.objects.filter(tag__slug=tag_slug, article_id=article.id).delete()
        # 태그의 카운트를 감소
        # tag = Tag.objects.filter(name=tag_name).first()
        # Tag.objects.filter(name=tag_name).update(count=F('count')+1)
        tag = Tag.objects.filter(slug=tag_slug).first()
        if tag.count > 1:
            tag.count -= 1
            tag.save()


    # 추가된 태그 항목에 대해서 생성하거나 변경
    for tag_slug in slugs_to_add_list:
        if len(tag_slug) > 0:
            tag_name = tag_list.get(tag_slug)
            if tag_name is not None:
                # tag, _ = Tag.objects.get_or_create(name=tag_name, slug=tag_slug)
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                tag_article = TagArticle(tag=tag, article_id=article.id)
                tag_article.save()
                # 태그의 카운트를 증가
                tag.count += 1
                tag.save()
