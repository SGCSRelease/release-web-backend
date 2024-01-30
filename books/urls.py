from django.urls import path

from . import views

urlpatterns = [
    path('list', views.list_book, name='list_book'),
    path('image', views.get_image, name='get_image'),
    path('borrow', views.borrow, name='borrow'),
]