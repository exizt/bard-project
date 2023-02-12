from django.contrib import admin
from .models import *
from django import forms
from django.forms import ModelForm

# Register your models here.
# admin.site.register(Article)
# admin.site.register(ArticleContent)


class ArticleContentInline(admin.StackedInline):
    model = ArticleContent


class ArticleSectionInline(admin.StackedInline):
    model = SectionArticle


class ArticleTagInline(admin.TabularInline):
    model = TagArticle
    verbose_name = "태그"
    verbose_name_plural = "태그 목록"


class ArticleAdminForm(forms.ModelForm):
    # 태그
    tag_input = forms.CharField(label='태그', required=False, 
        help_text="입력 예시: python, article",
        widget=forms.TextInput(attrs={'size':80}))

    # 본문
    markdown = forms.CharField(label="본문 (마크다운)", 
        widget=forms.Textarea(attrs={'rows': 50, 'cols': 100}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.id is not None:
            article_content = ArticleContent.objects.filter(article_id=self.instance.id).first()
            if article_content is not None:
                self.fields["markdown"].initial = article_content.markdown
            tags = TagArticle.objects.filter(article_id=self.instance.id).all()
            if tags is not None:
                pass

    def save(self, commit=True):
        # article = super(ArticleAdminForm, self).save(commit=commit)
        # article = super(ArticleAdminForm, self).save(commit=commit)
        article = super(ArticleAdminForm, self).save(commit=True)
        
        # content_markdown = self.cleaned_data.get("markdown")

        # self.instance.tag_input = self.cleaned_data.get('tag_input')
        #   

        # content_obj = ArticleContent(article_id=self.instance.pk, markdown = content_markdown)
        # content_obj.save()


        # self.instance.content = ArticleContent(article=self.instance, markdown=content_markdown)

        # article.content = ArticleContent(article=self.instance, markdown=content_markdown) 
        # article_content 
        # content_obj = ArticleContent(article=article, markdown=content_markdown)
        #if content_obj.article_id is not None:
        #    content_obj.save()
        # content_obj.save()

        # obj, created = ArticleContent.objects.update_or_create(
        #    article_id=instance.id,
        #    markdown=content_markdown
        # )
        return article
    
    def save_m2m(self):
        cleaned_data = self.cleaned_data
        article_id = self.instance.pk

        # content 테이블
        content_markdown = cleaned_data.get("markdown")
        content_obj = ArticleContent(article_id=article_id, markdown=content_markdown)
        content_obj.save()

        super(ArticleAdminForm, self)._save_m2m()


    class Meta:
        model = Article
        # fields = ('title',' slug', 'summary')
        exclude = ('created_at', 'updated_at')
        # widgets = { 'title': forms.TextInput(attrs={'size':80})}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    
    list_display = ['title', 'status', 'created_at', 'published_at']
    list_filter = ('status',)
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'summary', 'markdown')
        }),
        ('구분', {
            'fields': ('tag_input', )
        }),
        ('발행 상태', { 'fields': ('status', 'published_at')})
    )
    inlines = [ArticleSectionInline]
    # inlines = [ArticleSectionInline, ArticleContentInline]
    # inlines = [ArticleSectionInline, ArticleContentInline, ArticleTagInline]
    form = ArticleAdminForm


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ["name"]

