from django.shortcuts import render
from django.http import Http404


def index(request):
    if request.user.is_authenticated:
        return render(request, "adm/index.html")
    else:
        raise Http404()


