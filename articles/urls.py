from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.all_posts, name = "all_posts"),
    path('create/', views.create_post, name = "create_post"),
    path('<slug:slug>', views.detailed_post, name = "detailed_post"),
    path('<slug:slug>/edit', views.edit_post, name='edit_post'),
    path('<slug:slug>/delete', views.delete_post, name='delete_post'),
]
