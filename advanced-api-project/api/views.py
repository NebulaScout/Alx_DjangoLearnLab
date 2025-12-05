from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
from rest_framework import filters

from .serializers import BookSerializer, AuthorSerializer
from .models import Book, Author

class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class ListView(generics.ListAPIView):
    """
    List all books with filtering, searching, and ordering capabilities.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Filter backends - enable searching and ordering functionality
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    
    # Fields that support exact match filtering
    filterset_fields = ["title", "author", "publication_year"]
    
    # Fields that support text search (case-insensitive, partial matching)
    # Searches across title field and related author name field
    search_fields = ["title", "author__name"]
    
    # Fields that support ordering
    ordering_fields = ["title", "publication_year"]

class DetailView(generics.ListAPIView):
    """Get detailed info on a book"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class CreateView(generics.CreateAPIView):
    """Create a book"""
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class UpdateView(generics.UpdateAPIView):
    """Update book info"""
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"

class DeleteView(generics.DestroyAPIView):
    """Delete a book"""
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
