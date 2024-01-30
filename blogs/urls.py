from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.index, name="home"),
    path('newPost', views.newPost, name="newPost"),
    path('get_blogs/', views.get_blogs, name='get_blogs'),
    path('blog_detail/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('blog_delete/<int:blog_id>/', views.delete_post, name='delete_post'),
    path('get_blog_data/<int:blog_id>/', views.get_blog_data, name='get_blog_data'),
    path('get_user_name/', views.get_user_name, name="get_user_name"),
    path('editPost/<int:blog_id>/', views.editPost, name="editPost"),
]