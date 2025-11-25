from django.shortcuts import render
from rest_framework import generics
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    pass