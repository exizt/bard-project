from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(Article)
# admin.site.register(ArticleContent)


class ArticleContentInline(admin.StackedInline):
    model = ArticleContent


class ArticleSectionInline(admin.StackedInline):
    model = SectionArticle


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'created_at', 'published_at']
    list_filter = ('status',)
    inlines = [ArticleSectionInline, ArticleContentInline]


# admin.site.register(Article, ArticleAdmin)
