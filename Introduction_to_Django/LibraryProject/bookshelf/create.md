### Creating a Book Instance

**Command:**
new_book = Book.objects.create(title='1984', author='George Orwell', publication_year=1949)
print(f"Created book: {new_book.title} by {new_book.author} (ID: {new_book.id})")

**Output:**

Created book: 1984 by George Orwell (ID: 1)
