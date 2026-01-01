from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.routers import DefaultRouter

from . import views
from .views import ListView, DetailView, CreateView, UpdateView, DeleteView

app_name = 'blog'


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='blog/base.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    # Posts
    path('posts/', ListView.as_view(), name='posts'),
    path('posts/<int:pk>/', DetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', UpdateView.as_view(), name='edit_post'),
    path('post/new/', CreateView.as_view(), name='create_post'),
    path('post/<int:pk>/delete/', DeleteView.as_view(), name='delete_post'),
]