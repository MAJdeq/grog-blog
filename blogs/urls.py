from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.index, name="home"),
    path('newPost', views.newPost, name="newPost"),
    path('get_blogs/', views.get_blogs, name='get_blogs'),
    path('blog/detail/<int:blog_id>/', views.blog_detail, name='blog_detail'),
]