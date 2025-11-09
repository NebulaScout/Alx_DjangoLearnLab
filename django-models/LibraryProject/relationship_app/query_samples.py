from typing import Optional
from django.core.exceptions import ObjectDoesNotExist


def get_books_by_author(author_id: int = None, author_name: str = None):
    """Return all Book instances for the given author.

    Provide either `author_id` or `author_name`. Returns an empty queryset when
    the author does not exist.
    """
    if author_id is None and author_name is None:
        raise ValueError("Provide author_id or author_name")

    # import models lazily to avoid Django app registry errors on import
    from relationship_app.models import Author, Book

    try:
        if author_id is not None:
            author = Author.objects.get(pk=author_id)
        else:
            author = Author.objects.get(name=author_name)
    except Author.DoesNotExist:
        return Book.objects.none()

    return Book.objects.filter(author=author)


def get_books_in_library(library_id: int = None, library_name: str = None):
    """Return all Book instances stored in the given Library.

    Provide either `library_id` or `library_name`. Returns an empty queryset
    when the library does not exist.
    """
    if library_id is None and library_name is None:
        raise ValueError("Provide library_id or library_name")

    from relationship_app.models import Library, Book

    try:
        if library_id is not None:
            library = Library.objects.get(pk=library_id)
        else:
            library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return Book.objects.none()

    # ManyToManyField on Library named 'books'
    return library.books.all()


def get_librarian_for_library(library_id: int = None, library_name: str = None) -> Optional[object]:
    """Return the Librarian for the given Library, or None if none exists.

    Provide either `library_id` or `library_name`.
    """
    if library_id is None and library_name is None:
        raise ValueError("Provide library_id or library_name")

    from relationship_app.models import Library, Librarian

    try:
        if library_id is not None:
            library = Library.objects.get(pk=library_id)
        else:
            library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return None

    try:
        return getattr(library, "librarian")
    except ObjectDoesNotExist:
        try:
            return Librarian.objects.get(library=library)
        except Librarian.DoesNotExist:
            return None


if __name__ == "__main__":

    import os
    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
    django.setup()

    # Example usage (will print empty lists/None when objects are missing):
    print("Books by author 'Jane Doe':", list(get_books_by_author(author_name="Jane Doe")))
    print("Books in library 'Central':", list(get_books_in_library(library_name="Central")))
    first_lib = None
    from relationship_app.models import Library
    first_lib = Library.objects.first()
    if first_lib:
        print("Librarian for first library:", get_librarian_for_library(library_id=first_lib.id))
    else:
        print("No libraries found in database.")
