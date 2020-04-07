from django.urls import path
from .views import all_posts, create_post, detailed_post, edit_post, delete_post

app_name = 'articles'

urlpatterns = [
    path('', all_posts, name = "all_posts"),
    path('create/', create_post, name = "create_post"),
    path('<slug:slug>', detailed_post, name = "detailed_post"),
    path('<slug:slug>/edit', edit_post, name='edit_post'),
    path('<slug:slug>/delete', delete_post, name='delete_post'),
]
