from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import Book, Author
from accounts.models import User

class BookCRUDTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(username="admin", email="admin@test.com", password="adminPass")
        self.normal_user = User.objects.create_user(username="user", email="user@test.com", password="userPass")
        self.author = Author.objects.create(name="Jane Austen")
        self.book = Book.objects.create(
            title="Pride and Prejudice",
            publication_year=1813,
            author=self.author
        )

    # LIST - Test getting all books
    def test_list_books(self):
        url = reverse('get-all-books')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.json()), 1)
        # response.data

    # RETRIEVE - Test getting a single book
    def test_retrieve_book(self):
        url = reverse('book-detail', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['title'], self.book.title)

    # CREATE - Test creating a new book
    def test_create_book_unauthenticated(self):
        url = reverse('create-book')
        data = {
            "title": "Sense and Sensibility",
            "publication_year": 1811,
            "author": self.author.id # type: ignore
        } 
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_authenticated(self):
        url = reverse('create-book')
        data = {
            "title": "Sense and Sensibility",
            "publication_year": 1811,
            "author": self.author.id # type: ignore
        }
        # self.client.login(username="admin", password="adminPass")
        self.client.force_login(user=self.admin_user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['title'], "Sense and Sensibility")
        self.assertEqual(Book.objects.count(), 2)

    # UPDATE - Test updating a book
    def test_update_book_unauthenticated(self):
        url = reverse('update-book', kwargs={"id": self.book.pk})
        data = {"title": "Pride & Prejudice"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_authenticated(self):
        url = reverse('update-book', kwargs={"id": self.book.pk})
        data = {
            "title": "Pride & Prejudice",
            "publication_year": 1813,
            "author": self.author.id # type: ignore
        }
        self.client.force_login(user=self.admin_user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], "Pride & Prejudice")
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Pride & Prejudice")

    def test_partial_update_book(self):
        url = reverse('update-book', kwargs={"id": self.book.pk})
        data = {"title": "Pride & Prejudice - Updated"}
        self.client.force_login(user=self.admin_user)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Pride & Prejudice - Updated")

    # DELETE - Test deleting a book
    def test_delete_book_unauthenticated(self):
        url = reverse('delete-book', kwargs={'pk': self.book.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 1)

    def test_delete_book_authenticated(self):
        url = reverse('delete-book', kwargs={'pk': self.book.pk})
        self.client.force_login(user=self.admin_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    # FILTERING - Test filtering functionality
    def test_filter_books_by_author(self):
        url = reverse('get-all-books')
        response = self.client.get(url, {'author': self.author.id}) # type: ignore
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_search_books(self):
        url = reverse('get-all-books')
        response = self.client.get(url, {'search': 'Pride'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.json()), 1)

    def test_order_books(self):
        Book.objects.create(title="Emma", publication_year=1815, author=self.author)
        url = reverse('get-all-books')
        response = self.client.get(url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        books = response.json()
        self.assertEqual(books[0]['publication_year'], 1813)

