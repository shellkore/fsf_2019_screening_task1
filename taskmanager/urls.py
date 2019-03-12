from taskmanager import views
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
  