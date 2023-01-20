from django.shortcuts import render
from .models import *


def index(request):
    """

    :param request:
    :return:
    """
    articles = Article.objects.all()

    from django.conf import settings
    ips = settings.INTERNAL_IPS
    rem = get_client_ip(request)
    return render(request, 'blog/list.html', {'ips': ips, 'rem': rem})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
