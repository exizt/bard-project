from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import *
from django.conf import settings
from django.http import Http404


def index(request):
    """

    :param request:
    :return:
    """
    # articles = Article.objects.filter(status=1).order_by('-published_at')
    # articles = Article.objects.filter(status=1).order_by('-published_at')
    articles = Article.objects.prefetch_related('tags').filter(status=1).order_by('-published_at')

    context = {
        'articles': articles,
        'blog': get_blog_info()
    }
    skin_name = settings.BLOG_SKIN
    return render(request, f'{skin_name}/list.html', context)


def view(request, slug):
    # article = Article.objects.filter(slug=slug).first()
    article_qry = Article.objects.filter(slug=slug)

    article = get_object_or_404(article_qry)
    # article_content = ArticleContent.objects.filter(article=article).first()
    article_content = article.content.markdown
    tags = article.tags.all()


    # view에서 이용될 obj(dict)
    article_vo = {
        'id': article.id,
        'published_at': article.published_at,
        'summary': article.summary,
        'title': article.title,
        'tags': tags,
        'content_markdown': article_content
    }

    context = {
        'article': article_vo,
        'article_origin': article,
        'blog': get_blog_info()
    }
    skin_name = settings.BLOG_SKIN
    return render(request, f'{skin_name}/article.html', context)


def index_by_category(request, slug):
    """
    섹션 카테고리에 의한 게시물 목록
    """
    section = Section.objects.filter(slug=slug).first()

    if section is None:
        raise Http404()
        # return HttpResponseNotFound()
    else:
        articles = Article.objects.filter(section__id=section.id, status=1).order_by('-published_at')
        # articles = Article.objects.filter(tag__id=1).order_by('-published_at')
        # articles = Article.objects.filter(status=1).order_by('-published_at')
        # articles = Article.objects.filter(status=1, tag=tag).order_by('-published_at')

    context = {
        'articles': articles,
        'blog': get_blog_info()
    }
    skin_name = settings.BLOG_SKIN
    return render(request, f'{skin_name}/list.html', context)


def get_blog_info():
    return {
        'logo_str': '언제나초심',
        'logo': '',
        'logos': {
            'icon': '',
            'wordmark': '',
            'sitetitle': '언제나초심'
        }
    }

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
