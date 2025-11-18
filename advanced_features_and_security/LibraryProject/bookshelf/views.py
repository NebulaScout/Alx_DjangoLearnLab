from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.forms import ModelForm
from django import forms

from .models import Book
from .forms import ExampleForm, BookForm


def example_form_view(request):
    """
    Example view demonstrating ExampleForm usage
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process the form data
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            email = form.cleaned_data['email']
            published_date = form.cleaned_data['published_date']
            is_published = form.cleaned_data['is_published']
            
            messages.success(request, f'Form submitted successfully! Title: {title}')
            return redirect('book_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})


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

