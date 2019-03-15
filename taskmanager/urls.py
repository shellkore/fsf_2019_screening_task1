from django.urls import path
from django.conf.urls import url,include
from taskapp import views
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings
#from taskapp.views import AutocompleteJsonView
urlpatterns = [
    path('', views.home,name='home'),

    # Team urls
    url(r'^team/create/$', views.teamreg,name='teamreg'),
    url(r'^team/view/(?P<string>.+)/$', views.teamview,name='teamview'),
    url(r'^team/edit/(?P<string>.+)/$', views.teamedit,name='teamedit'),
    
    # Task urls
    url(r'^task/create/$', views.taskreg,name='taskreg'),
    url(r'^task/view/(?P<string>.+)/$', views.taskview,name='taskview'),
    url(r'^task/edit/(?P<string>.+)/$', views.taskedit,name='taskedit'),
    url(r'^task/delete/(?P<string>.+)/$', views.taskdelete,name='taskdelete'),
    
    # Comments urls
    url(r'^comment/edit/(?P<id>[\w\-]+)/$', views.commentedit,name='commentedit'),
    url(r'^comment/delete/(?P<id>[\w\-]+)/$', views.commentdel,name='commentdel'),
    
    # Ajax requests urls
    url(r'^ajax/users/$', views.users_list, name='users_list'),
    url(r'^ajax/team/users/$', views.team_users_list, name='team_users_list'),
    url(r'^ajax/teams/$', views.teams_list, name='teams_list'),
    
]