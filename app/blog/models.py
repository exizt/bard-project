from django.db import models
# from custom_field import *
# import custom_field
# from . import custom_field
# from . import custom_field
from .custom_field import *
from django.utils.timezone import now
from django.dispatch import receiver
from django.db.models.signals import post_save


class Article(models.Model):
    """
    게시물 테이블
    """
    class Status(models.IntegerChoices):
        TRASH = 0  # 휴지통.
        PUBLISH = 1  # 공개/발행
        FUTURE = 2  # 발행 예정
        DRAFT = 3  # 초안. 미완성 글.
        PENDING = 4  # 보류 중
        PRIVATE = 5  # 사적인 글. 비공개 글.
        AUTO_DRAFT = 6  # 자동 저장된 초안.

    id = UnsignedAutoField(primary_key=True)
    # article title
    title = models.CharField("제목", max_length=255, default='', help_text="게시글 제목 입니다.")
    # slug for article url
    slug = models.SlugField(max_length=200, default='', unique=True)
    # 본문 요약
    summary = models.CharField("요약", max_length=255, default='', help_text="게시글 요약글 입니다.")
    # 발행 여부 (기본값 false)
    is_published = models.BooleanField(default=False)
    # 싱테
    status = models.IntegerField("상태", choices=Status.choices, default=Status.DRAFT,
                                 help_text="게시글 상태 : publish (발행, 공개), draft (임시)")
    # dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField("발행일시", default=now)

    class Meta:
        db_table = "articles"
        indexes = [
           models.Index(fields=['-published_at'])
        ]
    
    def get_absolute_url(self):
        """관리자 페이지에서 '사이트에서 보기' 링크 """
        return f"/articles/{self.slug}"


@receiver(post_save, sender=Article)
def create_article_content(sender, instance, created, **kwargs):
    if created:
        ArticleContent.objects.create(article=instance)


class ArticleContent(models.Model):
    """
    게시물 컨텐츠 테이블.
    History 기능 지원을 고려, PK는 Auto Increment bigint id로 두도록 함.
    """
    article = models.OneToOneField(
        Article,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    markdown = models.TextField("마크 다운", default='', blank=True)
    output = models.TextField("HTML 아웃풋", default='', blank=True)
    # article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        db_table = "article_content"


#
class Tag(models.Model):
    id = UnsignedAutoField(primary_key=True)
    name = models.CharField(max_length=255, default='')
    slug = models.CharField(max_length=255, default='')
    # articles = models.ManyToManyField(Article, db_table="tag_article_rel")
    articles = models.ManyToManyField(Article,
                                      through="TagArticle",
                                      related_name="tag")
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


#
class Section(models.Model):
    id = UnsignedAutoField(primary_key=True)
    name = models.CharField("섹션 명칭", max_length=255, default='')
    # slug = models.CharField(max_length=255, default='')
    slug = models.SlugField(max_length=200, default='', unique=True)
    description = models.CharField("섹션 요약 설명", max_length=255, default='')
    logical_path = models.CharField(max_length=255, default='')
    order = models.IntegerField("정렬 순", default=0)
    depth = models.IntegerField("깊이", default=0)
    count = models.IntegerField("글 수", default=0, editable=False)
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
    section = models.ForeignKey(Section, verbose_name="섹션 카테고리", on_delete=models.SET_NULL, null=True)

    # dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "section_article_rel"
        indexes = [
            models.Index(fields=['section_id'])
        ]
