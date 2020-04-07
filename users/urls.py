from django.urls import path

from .views import sign_in, sign_up, sign_out, profile, edit_profile, change_password

app_name = 'users'

urlpatterns = [
    path('sign_in/', sign_in, name='sign_in'),
    path('sign_up/', sign_up, name='sign_up'),
    path('sign_out/', sign_out, name='sign_out'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/change_password/', change_password, name='change_password'),
    # path('articles/', article_list, name='user_article_list'),
]
