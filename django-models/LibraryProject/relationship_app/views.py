from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from .models import Library, Book, UserProfile

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
    return user.is_authenticated and user.role == 'admin'

def is_librarian(user):
    return user.ia_authenticated and user.role == 'librarian'

def is_member(user):
    return user.is_authenticated and user.role == 'member'

@user_passes_test(is_admin)
def admin_view(request):
    template_name = "relationship_app/admin_view.html"
    return render(request, template_name)

@user_passes_test(is_librarian)
def librarian_view(request):
    template_name = "relationship_app/librarian_view.html"
    return render(request, template_name)

@user_passes_test(is_member)
def member_view(request):
    template_name = "relationship_app/member_view.html"
    return render(request, template_name)