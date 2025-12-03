from rest_framework import serializers
from datetime import datetime

from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    """Serializes the book model"""
    class Meta:
        model = Book
        fields = '__all__'
    
    def validate_publication_year(self, value):
        """validate the publication year is not in the future"""
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year must be less than %d", current_year)
        elif value.len > 4:
            raise serializers.ValidationError("Invalid year")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """serialize author model"""
    books = BookSerializer(many=True) # show books associated with the author

    class Meta:
        model = Author
        fields = ['name', 'books']

