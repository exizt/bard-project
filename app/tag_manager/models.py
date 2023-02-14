from django.db import models
from blog.models import *


class Tag(models.Model):
    id = UnsignedAutoField(primary_key=True)
    name = models.CharField("태그명", max_length=255, default='', unique=True, 
                            help_text="태그명. url로 사용되므로, 소문자 + _ 로 구성되어야 한다.")
    # slug = models.CharField(max_length=255, default='')
    page_title = models.CharField("태그페이지 제목", max_length=255, default='', blank=True,
                                  help_text="페이지 상단에 노출될 태그 페이지의 제목. 없을 시 '태그명'이 표시됨.")
    # articles = models.ManyToManyField(Article, db_table="tag_article_rel")
    description = models.CharField("태그에 대한 요약 설명", max_length=255, default='', blank=True,
                                   help_text="")
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

    def get_absolute_url(self):
        """
        태그 페이지의 링크.
          - 관리자 페이지에서 '사이트에서 보기'
          - 글 목록에서 태그 클릭시 이동하는 링크
        """
        return f"/hashtags/{self.name}"


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
