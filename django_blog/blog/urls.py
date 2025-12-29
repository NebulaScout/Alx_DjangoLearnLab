from django.urls import path,include
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'blog'


urlpatterns =[
    path('', views.home, name='home'),
    path('register/', views.register, name = 'register'),
    path('login/', LoginView.as_view(template_name = 'blog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='blog/base.html'), name='logout'),
    path('profile/', views.profile, name='profile'),

]