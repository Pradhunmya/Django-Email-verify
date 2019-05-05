from django.urls import path,include
from .views import index,register,activate
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('index/',index,name='index'),
    path('login/',auth_views.login,{'template_name': 'login.html'},name='login'),
    path('register/',register,name='register'),
    path('activate/<uidb64>/<token>/',activate,name='activate'),
]