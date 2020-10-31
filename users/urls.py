from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.index),
    path('delete/<int:id>/', views.delete, name='delete-user'),
    path('changepassword/', views.change_password, name='changepassword'),
    path('enable/<int:id>/', views.enable, name='enable-user'),
]