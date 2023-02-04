from django.contrib import admin
from .models import *
from django import forms

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


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'created_at', 'published_at']
    list_filter = ('status',)
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'summary')
        }),
        ('발행 상태', { 'fields': ('status', 'published_at')})
    )
    # inlines = [ArticleSectionInline, ArticleContentInline]
    inlines = [ArticleSectionInline, ArticleContentInline, ArticleTagInline]


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ["name"]

