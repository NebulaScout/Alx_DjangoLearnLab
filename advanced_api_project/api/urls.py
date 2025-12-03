from django.urls import path

from .views import AuthorListCreateAPIView, BookListCreateAPIView

urlpatterns = [
    path('author/', AuthorListCreateAPIView.as_view()),
    path('book/', BookListCreateAPIView.as_view()),
]