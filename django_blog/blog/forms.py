from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from taggit.forms import TagWidget
from taggit.models import Tag

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
        fields = ["title", "content", "tags"]
        widgets = {
            'tags': TagWidget(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tags separated by commas (e.g., python, django, web)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If editing an existing post, populate the tags field
        if self.instance.pk:
            self.fields['tags'].initial = ', '.join(
                tag.name for tag in self.instance.tags.all()
            )

    def save(self, commit=True):
        post = super().save(commit=commit)
        
        if commit:
            # Clear existing tags and add new ones
            post.tags.clear()
            tags_input = self.cleaned_data.get('tags', '')
            
            if tags_input:
                tag_names = [name.strip().lower() for name in tags_input.split(',') if name.strip()]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)
        
        return post
        
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