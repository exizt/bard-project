from django.urls import path, re_path
from . import views

app_name = 'tags'
urlpatterns = [
    # path('', views.index),
    path('', views.index, name='index'),
    # path('<slug:tag_slug>/', views.index_by_tag, name='articles_by_tag'),
    # re_path(r'^(?P<tag_slug>[-a-z0-9\%\#]+)/$', views.index_by_tag, name='articles_by_tag'),
    re_path(r'^(?P<tag_slug>[-\w]+)/$', views.index_by_tag, name='articles_by_tag'),
]
