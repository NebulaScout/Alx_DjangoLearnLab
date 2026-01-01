# from django.shortcuts import render
# from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated, IsAdminUser

# from blog.models import Post
# from .serializers import PostSerializer

# class ListView(generics.ListAPIView):
#     """display all blog posts"""
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

# class DetailView(generics.ListAPIView):
#     """show individual blog posts"""
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

# class CreateView(generics.CreateAPIView):
#     """allow authenticated users to create new posts"""
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticated]

# class UpdateView(generics.UpdateAPIView):
#     """enable post authors to edit their posts."""
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticated]

# class DeleteView(generics.DestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticated, IsAdminUser]

