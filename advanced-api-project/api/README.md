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

## Authentication & Permissions

- Uses Django REST framework's built-in authentication
- Token-based authentication for API access
- Custom permissions for different user roles

## Error Handling

All views include proper error handling with appropriate HTTP status codes and error messages.
