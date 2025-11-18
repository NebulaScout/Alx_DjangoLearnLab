from django import forms
from .models import Book


class ExampleForm(forms.Form):
    """
    Example form demonstrating basic Django form functionality.
    """
    title = forms.CharField(
        max_length=200,
        label="Title",
        help_text="Enter the title of the item"
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        label="Description",
        help_text="Enter a detailed description"
    )
    email = forms.EmailField(
        label="Email Address",
        help_text="Enter a valid email address"
    )
    published_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Published Date",
        help_text="Select the publication date"
    )
    is_published = forms.BooleanField(
        required=False,
        label="Is Published",
        help_text="Check if this item is published"
    )


class BookForm(forms.ModelForm):
    """
    Model form for the Book model.
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'title': 'Enter the book title',
            'author': 'Enter the author name',
            'publication_year': 'Enter the year of publication',
        }
