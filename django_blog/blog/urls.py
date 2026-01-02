from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    CommentCreateView, CommentDeleteView, CommentUpdateView,
    PostSearchView, PostByTagListView
)

app_name = 'blog'


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='blog/base.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    # Posts
    path('posts/', PostListView.as_view(), name='posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='edit_post'),
    path('post/new/', PostCreateView.as_view(), name='create_post'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post'),
    # Comments
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='add_comment'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='edit_comment'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='delete_comment'),
    # Search
    path('search/', PostSearchView.as_view(), name='search'),
    # Tags
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='posts_by_tag'),
]