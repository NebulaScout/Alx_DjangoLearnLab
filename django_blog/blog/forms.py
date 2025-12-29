from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
        fields = '__all__'