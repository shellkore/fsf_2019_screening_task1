from django.urls import path
from django.conf.urls import url,include
from taskmanager import views
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home,name='home'),
]
