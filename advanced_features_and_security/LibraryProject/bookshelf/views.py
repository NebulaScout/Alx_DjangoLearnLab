from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.forms import ModelForm
from django import forms

from .models import Book


class BookForm(ModelForm):
    """Form for creating and editing books"""
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter book title',
                'required': True
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter author name',
                'required': True
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter publication year',
                'required': True
            }),
        }



@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    List all books 
    """
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail(request, book_id):
    """
    View details of a specific book 
    """
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'bookshelf/book_detail.html', {'book': book})


@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    Create a new book
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" was created successfully!')
            return redirect('book_detail', book_id=book.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_create.html', {'form': form})


@permission_required('bookshelf.can_change', raise_exception=True)
def book_edit(request, book_id):
    """
    Edit an existing book 
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" was updated successfully!')
            return redirect('book_detail', book_id=book.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_edit.html', {'form': form, 'book': book})


@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, book_id):
    """
    Delete a book 
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" was deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_delete.html', {'book': book})


def check_user_permissions(user):
    """
    Utility function to check what permissions a user has
    """
    return {
        'can_view': user.has_perm('bookshelf.can_view'),
        'can_create': user.has_perm('bookshelf.can_create'),
        'can_change': user.has_perm('bookshelf.can_change'),
        'can_delete': user.has_perm('bookshelf.can_delete'),
    }