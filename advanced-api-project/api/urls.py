from django.urls import path

from .views import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    AuthorListCreateAPIView
)

urlpatterns = [
    path('books/', ListView.as_view(), name='get-all-books'),
    path('books/<int:pk>/', DetailView.as_view(), name='book-detail'),
    path('books/create/', CreateView.as_view(), name='create-book'),
    path('books/update/<int:id>/', UpdateView.as_view(), name='update-book'),
    path('books/delete/<int:pk>/', DeleteView.as_view(), name='delete-book'),

    path('authors/', AuthorListCreateAPIView.as_view(), name='authors')
]