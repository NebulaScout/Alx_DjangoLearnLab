import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.urls import reverse_lazy


from blog.models import Post, Comment
from api.serializers import PostSerializer
from .forms import (
    RegistrationForm, 
    ProfileUpdateForm, 
    PostForm, 
    CommentForm)

@csrf_exempt
def register(request):
    print(f"requst method = {request.method}")
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print(f"Form has been called")
        print(f"Is form valid: {form.is_valid()}")
        if form.is_valid():
            print(f"Form is valid")
            form.save()
            messages.success(request, "Account created successfully")
            return redirect('blog:login')

        else:
            print(f"Form is invalid")
            print(f"Form errors: {form.errors}") 
            print(f"Form errors as JSON: {form.errors.as_json()}") 
            messages.error(request, "Form is invalid!!")
            # form = RegistrationForm()
    else:
        form = RegistrationForm()

    return render(request, 'blog/register.html', {'form': form})

def home(request):
    return render(request, 'blog/base.html')

@login_required
def profile(request):
    """View for users to view and edit their profile"""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user) # prefill with the current user data

        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully")
            return redirect('blog:profile')
        else:
            messages.error(request, "Unable to update your profile. Please correct any issues below.")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'blog/profile.html', {"form": form})

# Post views
class PostListView(generic.ListView):
    """Display all blog posts"""
    model = Post
    template_name = 'blog/posts_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']


class PostDetailView(generic.DetailView):
    """Display individual blog post"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all comments for this post, ordered by creation date
        context['comments'] = self.object.comments.all()
        # Provide the comment form for authenticated users
        context['comment_form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    """Allow authenticated users to create new posts"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'
    success_url = reverse_lazy('blog:posts')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    """Allow authors to update their posts"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit.html'
    context_object_name = 'post'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk}) # type: ignore

    def test_func(self):
        """Only allow the author to edit the post"""
        post = self.get_object()
        return self.request.user == post.author # type: ignore


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    """Allow authors to delete their posts"""
    model = Post
    template_name = 'blog/post_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('blog:posts')

    def test_func(self):
        """Only allow the author to delete the post"""
        post = self.get_object()
        return self.request.user == post.author # type: ignore
    
# Comment Views
class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    """Allow authenticated users to create comments on a post"""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        messages.success(self.request, "Comment added successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    """Allow comment authors to edit their comments"""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_edit.html'
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk}) # type: ignore

    def test_func(self):
        """Only allow the comment author to edit the comment"""
        comment = self.get_object()
        return self.request.user == comment.author # type: ignore

    def form_valid(self, form):
        messages.success(self.request, "Comment updated successfully!")
        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    """Allow comment authors to delete their comments"""
    model = Comment
    template_name = 'blog/comment_delete.html'
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk}) # type: ignore

    def test_func(self):
        """Only allow the comment author to delete the comment"""
        comment = self.get_object()
        return self.request.user == comment.author # type: ignore

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Comment deleted successfully!")