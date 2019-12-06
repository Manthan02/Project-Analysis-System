"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('register',views.register,name='register'),
    url('main',views.main,name='main'),
    url('login',views.login,name='login'),
    url('logout',views.logout,name='logout'),
    url('projects$',views.projects,name='projects'),
    url('tasks',views.tasks,name='tasks'),
    url('groups$',views.groups,name='groups'),
    path('groups/<int:group_id>',views.groupshow,name='groupshow'),
    url('friends',views.friends,name='friends'),
    url('requests$',views.requests,name='requests'),
    url('project_type',views.project_type,name='project_type'),
    url('private_add',views.private_add,name='private_add'),
    url('private_task_add',views.private_task_add,name='private_task_add'),
    url('public_task_add',views.public_task_add,name='public_task_add'),
    url('public_add',views.public_add,name='public_add'),
    url('addfriend',views.addfriend,name='addfriend'),
    url('addgroup',views.addgroup,name='addgroup'),
    url('addmember',views.addmember,name='addmember'),
    path('projects/<int:project_id>',views.projectshow,name='projectshow'),
    path('projects/<int:project_id>/<int:task_id>/1',views.to_do,name='to_do'),
    path('projects/<int:project_id>/<int:task_id>/2',views.in_pro,name='in_pro'),
    path('projects/<int:project_id>/<int:task_id>/3',views.done,name='done'),
    path('projects/<int:project_id>/addtask',views.addtask,name='addtask'),
    path('projects/<int:project_id>/backlog',views.backlog,name='backlog'),
    path('projects/<int:project_id>/chart',views.chart,name='chart'),
    path('projects/<int:project_id>/burndown',views.burndown,name='burndown'),
    path('requests/<int:friend_request_id>/accept',views.friend_accept,name='friend_accept'),
    path('requests/<int:friend_request_id>/decline',views.friend_decline,name='friend_decline'),
    path('requests/<int:group_request_id>/accept_group',views.group_accept,name='group_accept'),
    path('requests/<int:group_request_id>/decline_group',views.group_decline,name='group_decline'),
]
