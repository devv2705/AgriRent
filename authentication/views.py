from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate , login , logout
from .models import usersdata
def signin(request):
    if request.method == "POST":
        username=request.POST.get('email')
        password=request.POST.get('pass')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
        else:
            messages.error(request, "Invalid credentials")
            return redirect('/signin/')
    return render(request, 'authentication/signin.html')

def signup(request):
    if request.method == "POST":
        email=request.POST.get('email')
        aadhar=request.POST.get('aadharnumber')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        if pass1!=pass2:
            messages.error(request, "Passwords do not match")
            return redirect('/signup/')
        try:
            newuser=usersdata(email=email,aadharnumber=aadhar,password=pass1)
            newuser.save()
            messages.success(request, "Successfully created account")
            return redirect('/signin/')
        except IntegrityError:
            messages.error(request, "Email already exists")
            return redirect('/signup/')
        
    return render(request, 'authentication/signup.html')

def signout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/signin/')


def home(request):
    return render(request, 'home.html')