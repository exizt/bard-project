from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import *
from blog.models import *
from blog.utils import *
from django.http import Http404


def index(request):
    """
    태그 목록이 나타나는 페이지. 근데 이거 필요하나?
    """
    pass


def index_by_tag(request, tag_name):
    """
    태그에 의한 게시물 목록
    """
    tag = Tag.objects.filter(name=tag_name).first()

    if tag is None:
        raise Http404()
        # return HttpResponseNotFound()
    else:
        articles = Article.objects.prefetch_related('tags').filter(tags__id=tag.id, status=1).order_by('-published_at')
        # articles = Article.objects.filter(tag__id=1).order_by('-published_at')
        # articles = Article.objects.filter(status=1).order_by('-published_at')
        # articles = Article.objects.filter(status=1, tag=tag).order_by('-published_at')

    context = {
        'articles': articles,
        'blog': get_blog_info()
    }
    skin_name = settings.BLOG_SKIN
    return render(request, f'{skin_name}/list.html', context)