from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate , login , logout
from .models import farmerdata
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
    print(request.method)
    if request.method == "POST":
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        print("password",pass1,pass2)
        if pass1!=pass2:
            return render(request, 'authentication/signup.html',{"massage":"password must be same"})
        try:
            fname=request.POST.get('fname')
            dob=request.POST.get('dob')
            email=request.POST.get('email')
            newfarmer=farmerdata(fname=fname,dob=dob,email=email,password=pass1)
            newfarmer.save()
            return redirect(request, 'authentication/signin.html')
        except IntegrityError:
            return render(request, 'authentication/signup.html',{"massage":"email is already registered with us"})
        
    print("insignup function")
    return render(request, 'authentication/signup.html')

def signout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/signin/')


def home(request):
    return render(request, 'home.html')