from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .serializers import BookSerializer
from .models import Book

class ListView(generics.ListAPIView):
    """List all books"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class DetailView(generics.ListAPIView):
    """Get detailed info on a book"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class CreateView(LoginRequiredMixin, generics.CreateAPIView):
    """Create a book"""
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class UpdateView(LoginRequiredMixin, generics.UpdateAPIView):
    """Update book info"""
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class DeleteView(generics.DestroyAPIView):
    """Delete a book"""
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
