from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books
from .views import LibraryDetailView

urlpatterns = [
    path('books/', list_books, name='list_books'),    
    path('library/', LibraryDetailView.as_view(), name='library_detail'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('signup/', views.register, name='register')
]
