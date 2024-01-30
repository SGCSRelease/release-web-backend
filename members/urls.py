from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('get-profile', views.get_profile, name='get_profile'),
    path('edit-profile', views.edit_profile, name='edit_profile'),
    path('edit-password', views.edit_password, name='edit_password'),
    path('logout', views.logout, name='logout'),
    path('list', views.list_member, name='list_member'),
]