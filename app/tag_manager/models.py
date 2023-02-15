from django.db import models
from blog.models import *
from tag_manager.utils_tag_name import tag_slugify

"""
태그 기능의 모델들.

태그 개념 (이 프로젝트에서의)
  - 게시글에서 태그는 여러 개 달 수 있다. 
  - 태그는 slug 또는 name을 중점적으로 이용한다. 
  - slug는 name의 특수문자나 공백 등을 치환하여, URL 주소값으로 이용하기 쉽게 가공한 것이다.
  - 리디렉션이 가능하다. (한글 파이썬과 영문 Python은 동일하므로)
"""
class Tag(models.Model):
    id = UnsignedAutoField(primary_key=True)
    name = models.CharField("태그명", max_length=255, default='', unique=True, 
                            help_text="태그명. 변경 시 slug 값도 같이 변경되므로 주의.")
    slug = models.SlugField(max_length=255, default='', unique=True, allow_unicode=True,
                            help_text="URL에서 이용되는 슬러그. 태그명에서 공백(-), 소문자화 등을 적용.")
    page_title = models.CharField("태그페이지 제목", max_length=255, default='', blank=True,
                                  help_text="(HTML 옵션) 태그 페이지의 상단에 보여질 제목글. 없을 시 '태그명'이 기본으로 표시됨.")
    # articles = models.ManyToManyField(Article, db_table="tag_article_rel")
    description = models.CharField("태그에 대한 요약 설명", max_length=255, default='', blank=True,
                                   help_text="(HTML 옵션) 태그 페이지에 보여질 설명글.")
    count = models.PositiveIntegerField("게시글 수", default=0, editable=False) # unsigned int
    # parent_id = models.PositiveIntegerField("", null=True, blank=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, default=None, null=True, blank=True, verbose_name="리디렉션",
                               help_text="리디렉션을 지정하면, 지정한 태그로 리디렉션 처리가 됩니다.")
    # Many-to-Many fields
    articles = models.ManyToManyField(Article,
                                      through="TagArticle",
                                      related_name="tags")
    # dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tags"
        verbose_name_plural = "해시태그"

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = tag_slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
        태그 페이지의 링크.
          - 관리자 페이지에서 '사이트에서 보기'
          - 글 목록에서 태그 클릭시 이동하는 링크
        """
        slug = self.slug.replace('#','%23')
        return f"/hashtags/{slug}"


class TagArticle(models.Model):
    """
    Tag와 Article의 n:m 릴레이션 테이블.

    기본 구조
      - article_id : FK이며, Article을 가리킨다. 
          Article이 삭제될 때 해당 row는 삭제된다. (불필요하기 때문)
      - tag_id : FK이며, Tag를 가리킨다. 
          Tag가 삭제될 때 해당 row는 삭제된다. (큰 의미가 없기 때문)
    """
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
