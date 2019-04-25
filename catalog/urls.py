from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url('^$', views.tasks_list),
    url('^create_task/', views.create_task),
    url(r'^task/(?P<pk>\d+)$', views.TaskDetailView.as_view(), name = 'task-detail'),
    url(r'task/(?P<pk>\d+)/create_description/$', views.create_description),
    url(r'task/(?P<pk>\d+)/update/$', views.update_task),
    url(r'task/(?P<pk>\d+)/delete/$', views.delete_task),
]
