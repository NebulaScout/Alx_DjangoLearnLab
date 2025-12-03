from django.shortcuts import render
from rest_framework import generics

from .serializers import AuthorSerializer, BookSerializer
from .models import Author, Book

class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
