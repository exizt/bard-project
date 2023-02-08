from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'adm'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='adm/login.html', next_page='/adm/'), name='login'),
]
