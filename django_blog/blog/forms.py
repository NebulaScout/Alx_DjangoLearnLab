from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from blog.models import Post, Comment

class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)    

    def clean(self):
        cleaned_data = super().clean()
        passwd = cleaned_data.get('password1')
        confirm_passwd = cleaned_data.get("password2")

        if passwd and confirm_passwd and passwd != confirm_passwd:
            self.add_error(confirm_passwd, "Passwords do not match")
        
        return cleaned_data
        
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class ProfileUpdateForm(forms.ModelForm):
    """Form for users to update their profile information"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        
class CommentForm(forms.ModelForm):
    """Form for creating and updating comments"""
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Write your comment here...'
        }),
        label='',
        min_length=1,
        max_length=1000
    )

    class Meta:
        model = Comment
        fields = ['content']