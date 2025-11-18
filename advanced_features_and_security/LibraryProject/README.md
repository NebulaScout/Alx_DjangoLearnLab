# Django Permissions Testing

### Groups and Permissions

- **Admins**: Can view, add, edit, and delete books (`can_view`, `can_create`, `can_change`, `can_delete`)
- **Editors**: Can view, add, and edit books (`can_view`, `can_create`, `can_change`)
- **Viewers**: Can only view books (`can_view`)
- **No Group**: No permissions (access denied to all operations)

### Test Users

- Username / Password
- `test_admin` / `testpass123` → Admins group
- `test_editor` / `testpass123` → Editors group
- `test_viewer` / `testpass123` → Viewers group
- `test_nogroup` / `testpass123` → No group assigned

## Setup Instructions

```bash
python manage.py setup_groups --reset # Set up groups and permissions

python manage.py create_test_users --reset # Create test users

```

## Testing Instructions

1. Start the development server:

```bash
    python manage.py runserver
```

2. Navigate to the login page:

   - URL: ``http://127.0.0.1:8000/relationship_app/login/`

3. Test each user systematically:

   For each test user, login and test the following URLs:

- View Books: `http://127.0.0.1:8000/bookshelf/`
- View Book Detail: `http://127.0.0.1:8000/bookshelf/book/<book_id>/`
- Add Book: `http://127.0.0.1:8000/bookshelf/book/create/`
- Edit Book: `http://127.0.0.1:8000/bookshelf/book/<book_id>/edit/`
- Delete Book: `http://127.0.0.1:8000/bookshelf/book/<book_id>/delete/`

### Command-Line Testing

You can also test permissions using Django's shell:

```bash
python manage.py shell
```

```python
# Check specific user permissions
user = CustomUser.objects.get(username='test_viewer')
print(f"Can view: {user.has_perm('bookshelf.can_view')}")
print(f"Can add: {user.has_perm('bookshelf.can_create')}")
print(f"Can change: {user.has_perm('bookshelf.can_change')}")
print(f"Can delete: {user.has_perm('bookshelf.can_delete')}")

# Check user's groups
print(f"Groups: {[g.name for g in user.groups.all()]}")
```

## Expected Outcomes

- **Admins**: Full access to all operations
- **Editors**: Access to view, add, and edit books; denied delete
- **Viewers**: Access only to view books; denied add, edit, and delete
- **No Group**: Denied access to all operations(Gets 403 Forbidden in the web view)
