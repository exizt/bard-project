from django.db import models
# from custom_field import *
# import custom_field
# from . import custom_field
# from . import custom_field
from .custom_field import *
from django.utils.timezone import now


class Article(models.Model):
    """
    게시물 테이블
    """
    id = UnsignedAutoField(primary_key=True)
    # article title
    title = models.CharField(max_length=255, default='')
    # slug for article url
    slug = models.CharField(max_length=255, default='')
    # 본문 요약
    summary = models.CharField(max_length=255, default='')
    # 발행 여부 (기본값 false)
    is_published = models.BooleanField(default=False)
    # dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=now)

    class Meta:
        db_table = "articles"
        indexes = [
           models.Index(fields=['-published_at'])
        ]


class ArticleContent(models.Model):
    """
    게시물 컨텐츠 테이블.
    History 기능 지원을 고려, PK는 Auto Increment bigint id로 두도록 함.
    """
    markdown = models.TextField(max_length=255, default='')
    output = models.TextField(max_length=255, default='')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        db_table = "article_content"


#
class Tag(models.Model):
    id = UnsignedAutoField(primary_key=True)
    name = models.CharField(max_length=255, default='')
    slug = models.CharField(max_length=255, default='')
    articles = models.ManyToManyField(Article, related_name="tag")
    # dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tags"


#
# class TagArticle(models.Model):
#    article = models.ForeignKey(Article, on_delete=models.CASCADE)
#    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
#    tag_name_cached = models.CharField(max_length=255, default='')
#    # dates
#    created_at = models.DateTimeField(auto_now_add=True)
#    updated_at = models.DateTimeField(auto_now=True)
#
#    class Meta:
#        db_table = "tag_article_rel"
#        # indexes = [
#        #    models.Index(fields=['tag_name', 'article_id'])
#        # ]


#
class Section(models.Model):
    id = UnsignedAutoField(primary_key=True)
    name = models.CharField(max_length=255, default='')
    slug = models.CharField(max_length=255, default='')
    description = models.CharField(max_length=255, default='')
    logical_path = models.CharField(max_length=255, default='')
    order = models.IntegerField(default=0)
    depth = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    # dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "section"


class SectionArticle(models.Model):
    """
    A relation to section of article.
    It has one row per article.
    섹션은 하나의 값을 갖는다. 값은 null(전체 영역) 이거나 특정 섹션이 된다.
    """
    # article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    article = models.OneToOneField(
        Article,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)

    # dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "section_article_rel"
        indexes = [
            models.Index(fields=['section_id'])
        ]
