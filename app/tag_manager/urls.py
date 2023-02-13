from django.urls import path
from . import views

app_name = 'tags'
urlpatterns = [
    # path('', views.index),
    path('', views.index, name='index'),
    path('<slug:tag_name>/', views.index_by_tag, name='articles_by_tag'),
]
