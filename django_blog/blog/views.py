import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, ProfileUpdateForm

@csrf_exempt
def register(request):
    print(f"requst method = {request.method}")
    if request.method == 'POST':
        print(f"POST data: {request.POST}")  # ADD THIS LINE
        form = RegistrationForm(request.POST)
        print(f"Form has been called")
        print(f"Is form valid: {form.is_valid()}")
        if form.is_valid():
            print(f"Form is valid")
            # data = {
            #     "username": form.cleaned_data['username'],
            #     "first_name": form.cleaned_data['first_name'],
            #     "last_name": form.cleaned_data['last_name'],
            #     "email": form.cleaned_data['email'],
            #     "password1": form.cleaned_data['password1'],
            #     "password2": form.cleaned_data['password2'],
            # }
            # print(f"Data is valid: {data}")
            # response = requests.post(f"{settings.BASE_URL}/api/blog/register/", json=data)

            # if response.status_code == status.HTTP_201_CREATED:
            #     messages.success(request, "Account created successfully")
            # else:
            #     messages.error(request, "Unable to create account!!")
            form.save()
            messages.success(request, "Account created successfully 👍")
            return redirect('blog:login')

        else:
            print(f"Form is invalid")
            print(f"Form errors: {form.errors}") 
            print(f"Form errors as JSON: {form.errors.as_json()}") 
            messages.error(request, "Form is invalid!!")
            # form = RegistrationForm()
    else:
        form = RegistrationForm()

    return render(request, 'blog/register.html', {'form': form})

def home(request):
    return render(request, 'blog/base.html')

@login_required
def profile(request):
    """View for users to view and edit their profile"""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user) # prefill with the current user data

        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully🥳")
            return redirect('blog:profile')
        else:
            messages.error(request, "Unable to update your profile. Please correct any issues below.")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'blog/profile.html', {"form": form})
