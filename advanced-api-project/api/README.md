# Advanced API Project - View Documentation

## Overview

This document provides detailed configuration and operational information for each API view in the advanced API project.

## View Configuration

### Book Views

#### ListView

- **Purpose**: Retrieve a list of all books with filtering, searching, and ordering capabilities
- **HTTP Method**: GET
- **Endpoint**: `/api/books/`
- **Features**:
  - Filtering by title, author, and publication year
  - Search functionality across title and author fields
  - Ordering by title and publication_year
- **Permissions**: Read-only access for all users

**Implementation Details:**

The ListView uses Django REST Framework's built-in filter backends:

**Filter Backends Configuration:**

- `filters.SearchFilter`: Enables search functionality
- `filters.OrderingFilter`: Enables ordering functionality
- `filterset_fields`: Fields available for exact filtering
- `search_fields`: Fields available for text search (supports related field lookups)
- `ordering_fields`: Fields available for sorting

**API Usage Examples:**

1. **Basic List (No Filters):**

   ```
   GET /api/books/
   ```

2. **Filtering by Exact Values:**

   ```
   GET /api/books/?title=The Great Gatsby
   GET /api/books/?publication_year=1925
   GET /api/books/?author=1  # Filter by author ID
   ```

3. **Text Search (Case-insensitive, partial matching):**

   ```
   GET /api/books/?search=gatsby
   GET /api/books/?search=fitzgerald  # Searches author names too
   GET /api/books/?search=great       # Searches in title field
   ```

4. **Ordering Results:**

   ```
   GET /api/books/?ordering=title              # Ascending by title
   GET /api/books/?ordering=-title             # Descending by title
   GET /api/books/?ordering=publication_year   # Ascending by year
   GET /api/books/?ordering=-publication_year  # Descending by year
   ```

5. **Combining Multiple Parameters:**
   ```
   GET /api/books/?search=the&ordering=-publication_year
   GET /api/books/?author=1&ordering=title
   GET /api/books/?publication_year=2020&search=python&ordering=-title
   ```

**Search Implementation Notes:**

- Search is performed using icontains lookup (case-insensitive partial matching)
- Multiple search terms are AND-ed together(e.g., `?search=python+django` finds books containing both terms)
- Search spans across both `title` field and related `author__name` field
- Special characters in search terms are automatically escaped

#### DetailView

- **Purpose**: Retrieve, update, or delete a specific book
- **HTTP Methods**: GET, PUT, PATCH, DELETE
- **Endpoint**: `/api/books/<id>/`
- **Permissions**: Read access for all users, write access for authenticated users

#### CreateView

- **Purpose**: Create a new book entry
- **HTTP Method**: POST
- **Endpoint**: `/api/books/create/`
- **Permissions**: Authenticated users only
- **Validation**: Custom validation for publication year

#### UpdateView

- **Purpose**: Update an existing book entry
- **HTTP Methods**: PUT, PATCH
- **Endpoint**: `/api/books/<id>/update/`
- **Permissions**: Authenticated users only

#### DeleteView

- **Purpose**: Delete a specific book entry
- **HTTP Method**: DELETE
- **Endpoint**: `/api/books/<id>/delete/`
- **Permissions**: Authenticated users only

## Filtering, Searching, and Ordering Features

### Overview

The API provides powerful filtering, searching, and ordering capabilities through Django REST Framework's filter backends. These features are primarily implemented in the `ListView` class.

### Filter Implementation

**Backend Configuration:**

```python
filter_backends = [filters.SearchFilter, filters.OrderingFilter]
filterset_fields = ["title", "author", "publication_year"]
```

**Available Filters:**

- `title`: Exact match filter for book titles
- `author`: Filter by author ID (foreign key relationship)
- `publication_year`: Exact match filter for publication year

### Search Implementation

**Backend Configuration:**

```python
search_fields = ["title", "author__name"]
```

**Search Behavior:**

- **Case-insensitive**: Searches ignore letter casing
- **Partial matching**: Finds books containing the search term
- **Cross-field search**: Searches both book titles and author names
- **Multiple terms**: Multiple search words are combined with AND logic

**Search Examples:**

```bash
# Find books with "django" in title or author name
curl "http://localhost:8000/api/books/?search=atomic"

# Find books by author containing "smith"
curl "http://localhost:8000/api/books/?search=jane"

# Multiple terms (must match all terms)
curl "http://localhost:8000/api/books/?search=python+programming"
```

### Ordering Implementation

**Backend Configuration:**

```python
ordering_fields = ["title", "publication_year"]
```

**Available Ordering:**

- `title`: Sort alphabetically by book title
- `publication_year`: Sort numerically by publication year
- Prefix with `-` for descending order

**Ordering Examples:**

```bash
# Sort by title A-Z
curl "http://localhost:8000/api/books/?ordering=title"

# Sort by title Z-A
curl "http://localhost:8000/api/books/?ordering=-title"

# Sort by publication year (newest first)
curl "http://localhost:8000/api/books/?ordering=-publication_year"
```

### Advanced Query Combinations

**Complex Filtering Examples:**

```bash
# Books from 1987, ordered by title
curl "http://localhost:8000/api/books/?publication_year=1987&ordering=title"

# Search for "python" books, newest first
curl "http://localhost:8000/api/books/?search=python&ordering=-publication_year"

# Books by specific author, alphabetically ordered
curl "http://localhost:8000/api/books/?author=1&ordering=title"

# Multiple filters with search and ordering
curl "http://localhost:8000/api/books/?search=web&publication_year=2021&ordering=-title"
```

### Error Handling

**Invalid Parameters:**

- Invalid field names in `ordering` parameter return 400 Bad Request
- Invalid data types (e.g., string for `publication_year`) return validation errors
- Unknown filter fields are ignored

## Authentication & Permissions

- Uses Django REST framework's built-in authentication
- Token-based authentication for API access
- Custom permissions for different user roles

## Error Handling

All views include proper error handling with appropriate HTTP status codes and error messages.

---

## Testing Documentation

### Testing Strategy

The API test suite follows a comprehensive approach to ensure all CRUD operations and API features work correctly. Tests are organized using Django REST Framework's `APITestCase` class and cover:

1. **CRUD Operations**: Complete coverage of Create, Read, Update, and Delete operations
2. **Authentication & Authorization**: Verification of permission requirements for protected endpoints
3. **Data Validation**: Testing API responses and data integrity
4. **Query Features**: Testing filtering, searching, and ordering capabilities

### Test Structure

**Test Class**: `BookCRUDTestCase`

**Test Fixtures** (`setUp` method):

- Creates test users (admin and normal user)
- Creates test author and book data
- Initializes API client for making requests

### Individual Test Cases

#### 1. LIST Operations

**Test**: `test_list_books`

- **Purpose**: Verify retrieval of all books
- **Endpoint**: `GET /api/books/`
- **Expected**: 200 OK status, returns list of books
- **Assertions**:
  - Status code is 200
  - Response contains at least one book

#### 2. RETRIEVE Operations

**Test**: `test_retrieve_book`

- **Purpose**: Verify retrieval of a single book by ID
- **Endpoint**: `GET /api/books/<pk>/`
- **Expected**: 200 OK status, returns specific book details
- **Assertions**:
  - Status code is 200
  - Response contains correct book title

#### 3. CREATE Operations

**Test**: `test_create_book_unauthenticated`

- **Purpose**: Verify unauthenticated users cannot create books
- **Endpoint**: `POST /api/books/create/`
- **Authentication**: None
- **Expected**: 403 Forbidden status
- **Assertions**:
  - Status code is 403

**Test**: `test_create_book_authenticated`

- **Purpose**: Verify authenticated users can create books
- **Endpoint**: `POST /api/books/create/`
- **Authentication**: Logged in as admin user
- **Payload**:
  ```json
  {
    "title": "Sense and Sensibility",
    "publication_year": 1811,
    "author": <author_id>
  }
  ```
- **Expected**: 201 Created status, book is created in database
- **Assertions**:
  - Status code is 201
  - Response contains correct book title
  - Book count increases by 1

#### 4. UPDATE Operations

**Test**: `test_update_book_unauthenticated`

- **Purpose**: Verify unauthenticated users cannot update books
- **Endpoint**: `PUT /api/books/update/<id>/`
- **Authentication**: None
- **Expected**: 403 Forbidden status
- **Assertions**:
  - Status code is 403

**Test**: `test_update_book_authenticated`

- **Purpose**: Verify authenticated users can fully update books (PUT)
- **Endpoint**: `PUT /api/books/update/<id>/`
- **Authentication**: Logged in as admin user
- **Payload**: Complete book data with updated title
- **Expected**: 200 OK status, book is updated in database
- **Assertions**:
  - Status code is 200
  - Response contains updated title
  - Database record is updated

**Test**: `test_partial_update_book`

- **Purpose**: Verify partial updates work (PATCH)
- **Endpoint**: `PATCH /api/books/update/<id>/`
- **Authentication**: Logged in as admin user
- **Payload**: Only the field(s) to update
  ```json
  {
    "title": "Pride & Prejudice - Updated"
  }
  ```
- **Expected**: 200 OK status, only specified fields are updated
- **Assertions**:
  - Status code is 200
  - Database record reflects the change

#### 5. DELETE Operations

**Test**: `test_delete_book_unauthenticated`

- **Purpose**: Verify unauthenticated users cannot delete books
- **Endpoint**: `DELETE /api/books/delete/<pk>/`
- **Authentication**: None
- **Expected**: 403 Forbidden status, book remains in database
- **Assertions**:
  - Status code is 403
  - Book count remains unchanged

**Test**: `test_delete_book_authenticated`

- **Purpose**: Verify authenticated users can delete books
- **Endpoint**: `DELETE /api/books/delete/<pk>/`
- **Authentication**: Logged in as admin user
- **Expected**: 204 No Content status, book is removed from database
- **Assertions**:
  - Status code is 204
  - Book count decreases by 1

#### 6. FILTERING Operations

**Test**: `test_filter_books_by_author`

- **Purpose**: Verify filtering books by author ID
- **Endpoint**: `GET /api/books/?author=<author_id>`
- **Expected**: 200 OK status, returns only books by specified author
- **Assertions**:
  - Status code is 200
  - Response contains exactly 1 book (matching test data)

#### 7. SEARCH Operations

**Test**: `test_search_books`

- **Purpose**: Verify text search across title and author fields
- **Endpoint**: `GET /api/books/?search=Pride`
- **Expected**: 200 OK status, returns books matching search term
- **Assertions**:
  - Status code is 200
  - Response contains at least 1 matching book

#### 8. ORDERING Operations

**Test**: `test_order_books`

- **Purpose**: Verify ordering books by publication year
- **Endpoint**: `GET /api/books/?ordering=publication_year`
- **Setup**: Creates additional book with different publication year
- **Expected**: 200 OK status, returns books in specified order
- **Assertions**:
  - Status code is 200
  - First book in response has earliest publication year

### Running the Tests

#### Run All Tests

```bash
python manage.py test
```

#### Run Specific Test Module

```bash
python manage.py test api.test_views
```

#### Run Specific Test Class

```bash
python manage.py test api.test_views.BookCRUDTestCase
```

#### Run Specific Test Method

```bash
python manage.py test api.test_views.BookCRUDTestCase.test_create_book_authenticated
```

#### Run with Verbose Output

```bash
python manage.py test api.test_views --verbosity=2
```

#### Run with Coverage Report

```bash
# Install coverage first
pip install coverage

# Run tests with coverage
coverage run --source='.' manage.py test api.test_views
coverage report
coverage html  # Generate HTML report
```
