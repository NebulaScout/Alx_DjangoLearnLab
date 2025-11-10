from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django import forms
from .models import Library, Book, UserProfile, Author

# Function-based view to list all books
def list_books(request):
    """
    Function-based view that lists all books in the database.
    Renders a template with book titles and their authors.
    """
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to display library details
class LibraryDetailView(DetailView):
    """
    Class-based view that displays details for a specific library,
    including all books available in that library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

def register(request):
    success_url = reverse_lazy("login")
    template_name = "relationship_app/register.html"

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, success_url)
    else:
        form = UserCreationForm()

    return render(request, template_name, {'form': form})

def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'member'

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }

@user_passes_test(is_admin)
@permission_required(['can_add_book', 'can_change_book', 'can_delete_book'])
def admin_view(request):
    template_name = "relationship_app/admin_view.html"
    return render(request, template_name)

@user_passes_test(is_librarian)
@permission_required(['can_add_book', 'can_change_book', 'can_delete_book'])
def librarian_view(request):
    template_name = "relationship_app/librarian_view.html"
    return render(request, template_name)

@user_passes_test(is_member)
def member_view(request):
    template_name = "relationship_app/member_view.html"
    return render(request, template_name)

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """
    View for adding a new book. Only users with 'can_add_book' permission can access.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('list_books')
    else:
        form = BookForm()
    
    return render(request, 'relationship_app/add_book.html', {'form': form})

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    """
    View for editing an existing book. Only users with 'can_change_book' permission can access.
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    """
    View for deleting a book. Only users with 'can_delete_book' permission can access.
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('list_books')
    
    return render(request, 'relationship_app/delete_book.html', {'book': book})