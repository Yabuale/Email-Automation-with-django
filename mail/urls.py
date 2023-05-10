from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name=''),
    path('mail/', views.mail, name='mail'),
    path('register/', views.register, name='register'),
    path('admin-register/', views.admin_register, name='admin_register'),
    path('admin-delete/', views.admin_delete, name='admin_delete'),
    path('send/', views.send, name='send'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('error/', views.error, name='error'),

]