from django.db import models

class Author(models.Model): 
    """Author details"""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Book(models.Model):
    """Book details"""
    title = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE) # one-to-many relationship between an author and books

    def __str__(self):
        return self.title