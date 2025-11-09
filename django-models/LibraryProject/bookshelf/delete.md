### Deleting a Book and Confirming Deletion

**Command:**

# Delete the book

from bookshelf.models import Book
book = Book.objects.filter(title='Nineteen Eighty-Four').first()
book.delete()

print(f"Deleted {book.title} book(s)")

**Output:**
Deleted 1 book(s)
