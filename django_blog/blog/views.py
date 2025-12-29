# import requests
from django.shortcuts import render
from django.contrib import messages

from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print(f"Form has been called")

        if form.is_valid():
            print(f"Form is valid")
            data = {
                "username": form.cleaned_data['username'],
                "first_name": form.cleaned_data['first_name'],
                "last_name": form.cleaned_data['last_name'],
                "email": form.cleaned_data['email'],
                "password1": form.cleaned_data['password1'],
                "password2": form.cleaned_data['password2'],
            }
            print(f"Data is valid: {data}")
            messages.success(request, "Data is valid")

        else:
            print(f"Form is invalid")
            messages.error(request, "Form is invalid!!")
            form = RegistrationForm()
    else:
        form = RegistrationForm()

    return render(request, 'blog/register.html', {'form': form})

def home(request):
    return render(request, 'blog/base.html')