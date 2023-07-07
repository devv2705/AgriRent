from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import IntegrityError
from .models import farmerdata
def signin(request):
    if request.method == "POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        #check in farmerdata model and authenticate
        user=farmerdata.objects.filter(email=email,password=password).first()
        if user is not None:
            messages.success(request, "Successfully logged in")
            return render(request, 'profile.html',{"name":user.fname,"email":user.email,"dob":user.dob})
        else:
            return render(request, 'authentication/signin.html',{"massage":"invalid credentials"})
    return render(request, 'authentication/signin.html')    


def signup(request):
    print(request.method)
    if request.method == "POST":
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        if pass1!=pass2:
            return render(request, 'authentication/signup.html',{"massage":"password must be same"})
        try:
            email=request.POST.get('email')
            fname=request.POST.get('fname')
            dob=request.POST.get('dob')
            newfarmer=farmerdata(fname=fname,dob=dob,email=email,password=pass1)
            newfarmer.save()
            return redirect('/signin/')
        except IntegrityError:
            return render(request, 'authentication/signup.html',{"massage":"email is already registered with us"})
    return render(request, 'authentication/signup.html')

def signout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/signin/')


def home(request):
    return render(request, 'home.html')