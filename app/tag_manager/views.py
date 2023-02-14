from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import *
from blog.models import *
from blog.utils import *
from django.http import Http404
from django.shortcuts import redirect


def index(request):
    """
    태그 목록이 나타나는 페이지. 근데 이거 필요하나?
    """
    pass


def index_by_tag(request, tag_slug):
    """
    태그에 의한 게시물 목록
    """
    # tag_slug = str(tag_slug).replace("#", "%23")
    tag = Tag.objects.filter(slug=tag_slug).first()

    # 생성되지 않은 태그명으로 접속한 경우 404로 처리.
    if tag is None:
        raise Http404()
        # return HttpResponseNotFound()
    
    # parent 값이 존재할 경우, 리디렉션을 한다.
    if tag.parent is not None:
        redirect_url = tag.parent.get_absolute_url()
        return redirect(redirect_url)

    # 태그와 하위 태그를 포함한 리스트
    tag_list = Tag.objects.filter(parent_id=tag.id).values_list('id', flat=True)
    tag_list = list(tag_list)
    tag_list.append(tag.id)


    # 해당하는 게시글 조회
    # articles = Article.objects.prefetch_related('tags').filter(tags__id=tag.id, status=1).order_by('-published_at')
    articles = Article.objects.prefetch_related('tags') \
        .filter(tags__id__in=tag_list, status=1) \
        .distinct() \
        .order_by('-published_at') \
        .only('title','slug','summary','published_at')
    # articles = qry.distinct().order_by('-published_at').only(cols)
    # articles = Article.objects.prefetch_related('tags').filter(tags__id__in=tag_list, status=1).distinct().order_by('-published_at')
    # articles = Article.objects.filter(tag__id=1).order_by('-published_at')
    # articles = Article.objects.filter(status=1).order_by('-published_at')
    # articles = Article.objects.filter(status=1, tag=tag).order_by('-published_at')

    context = {
        'articles': articles,
        'blog': get_blog_info()
    }
    skin_name = settings.BLOG_SKIN
    return render(request, f'{skin_name}/list.html', context)