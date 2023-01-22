from django.shortcuts import render
from .models import *
from django.conf import settings
from django.forms.models import model_to_dict


def index(request):
    """

    :param request:
    :return:
    """
    # articles = Article.objects.filter(status=1).order_by('-published_at')
    articles = Article.objects.filter(status=1).order_by('-published_at')

    context = {
        'articles': articles
    }
    skin_name = settings.BP_SKIN
    return render(request, f'{skin_name}/list.html', context)


def view(request, slug):
    article = Article.objects.filter(slug=slug).first()
    article_content = ArticleContent.objects.filter(article=article).first()

    # view에서 이용될 obj(dict)
    article_vo = {
        'id': article.id,
        'published_at': article.published_at,
        'summary': article.summary,
        'title': article.title,
        'content': article_content.output
    }

    context = {
        'article': article_vo,
        'article_origin': article,
    }
    skin_name = settings.BP_SKIN
    return render(request, f'{skin_name}/article.html', context)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
