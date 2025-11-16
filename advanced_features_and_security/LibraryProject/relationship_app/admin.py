from django.contrib import admin
from .models import Author, Librarian, Library, Book

# Register models with basic admin
admin.site.register(Librarian)
admin.site.register(Library)
admin.site.register(Author)
admin.site.register(Book)
