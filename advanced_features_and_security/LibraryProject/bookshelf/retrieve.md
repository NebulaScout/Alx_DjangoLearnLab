### Retrieving and Displaying All Attributes

**Command:**

book_data = Book.objects.get(title='1984')
print(book_data)

**Output:**

```
{'id': 1, 'title': '1984', 'author': 'George Orwell', 'publication_year': 1949}
```
