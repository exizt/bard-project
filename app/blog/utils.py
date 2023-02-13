from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import *
from django.conf import settings
from django.http import Http404


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
