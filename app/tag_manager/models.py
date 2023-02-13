from django.db import models
from blog.models import *


class Tag(models.Model):
    id = UnsignedAutoField(primary_key=True)
    name = models.CharField("태그명", max_length=255, default='', unique=True)
    # slug = models.CharField(max_length=255, default='')
    page_title = models.CharField("태그페이지 제목", max_length=255, default='')
    # articles = models.ManyToManyField(Article, db_table="tag_article_rel")
    description = models.CharField("태그에 대한 요약 설명", max_length=255, default='', blank=True)
    count = models.IntegerField("게시글 수", default=0, editable=False)
    # Many-to-Many fields
    articles = models.ManyToManyField(Article,
                                      through="TagArticle",
                                      related_name="tags")
    # dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tags"


class TagArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # tag_name_cached = models.CharField(max_length=255, default='')
    # dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tag_article_rel"
        indexes = [
           # models.Index(fields=['tag_name_cached', 'article_id'])
        ]
