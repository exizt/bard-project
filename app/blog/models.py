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
    
    기본 구조
      - id : 게시글 id
      - status : 게시글 상태값
      - slug : 유니크 인덱스
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
        verbose_name_plural = "게시글"

    def get_absolute_url(self):
        """관리자 페이지에서 '사이트에서 보기' 링크 """
        return f"/{self.slug}"
        # return f"/articles/{self.slug}"


@receiver(post_save, sender=Article)
def create_article_content(sender, instance, created, **kwargs):
    """
    one-to-one 관계의 ArticleContent에 컬럼을 하나 생성하는 기능.
    article이 생성이 되면 강제로 ArticleContent를 최소 하나 생성해준다.
    """
    if created:
        ArticleContent.objects.get_or_create(article=instance)
        SectionArticle.objects.get_or_create(article=instance)


class ArticleContent(models.Model):
    """
    게시물 컨텐츠 테이블.
    
    article_id를 PK + FK로 구성
    향후에 히스토리 기능을 지원할 지 고려 중.
    """
    article = models.OneToOneField(
        Article,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="content"
    )
    markdown = models.TextField("마크 다운", default='', blank=True)
    output = models.TextField("HTML 아웃풋", default='', blank=True)
    # article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        db_table = "article_content"


class Section(models.Model):
    """
    섹션 테이블
    게시글의 카테고리(섹션)을 담당한다
    카테고리와는 조금 다르게 깊이는 1 이상이 되지 않도록 한다
    """
    id = UnsignedAutoField(primary_key=True)
    name = models.CharField("섹션 명칭", max_length=255, default='')
    # slug = models.CharField(max_length=255, default='')
    slug = models.SlugField(max_length=200, default='', unique=True)
    description = models.CharField("섹션 요약 설명", max_length=255, default='')
    logical_path = models.CharField(max_length=255, default='')
    order = models.IntegerField("정렬 순", default=0)
    depth = models.IntegerField("깊이", default=0)
    count = models.IntegerField("게시글 수", default=0, editable=False)
    # dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "section"
        verbose_name_plural = "분야(섹션)"

    def __str__(self):
        return self.name


class SectionArticle(models.Model):
    """
    Article과 Section의 1:N 릴레이션 테이블.
    Article과의 관계는 1:1이고, Section과의 관계는 1:N(Section:SectionArticle)이다.

    기본 구조
      - article_id : PK로 사용되고, 인덱싱의 수월함을 위해서 
          게시글 생성시 같이 생성되고 삭제시 같이 삭제되게 한다.
      - section_id : FK이며, Section을 가리킨다.
          null 허용이어야 한다. (섹션을 지정하지 않을 수 있으므로)
    """
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
