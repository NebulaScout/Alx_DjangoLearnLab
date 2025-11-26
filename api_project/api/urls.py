from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .views import BookList, BookViewSet

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('token/', views.obtain_auth_token),
    path('books/', BookList.as_view(), name = 'book-list'),
    path('', include(router.urls)),
]