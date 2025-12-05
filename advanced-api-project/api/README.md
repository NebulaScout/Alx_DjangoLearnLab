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
