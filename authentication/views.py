from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import IntegrityError
from .models import farmer
import smtplib
from email.message import EmailMessage
import random

def send_mail(email,otp,n):
    server = smtplib.SMTP('smtp.gmail.com', '587')
    msg = EmailMessage()
    msg['From'] = "smitkunpara@gmail.com"
    msg['To'] = email
    if n == 1:
        msg.set_content(f'{otp} is you otp for signup verifiaction\nDont not share with anyone\nThank you Agrirent Team')
        msg['Subject'] = f'OTP for Agrirent verification'
    elif n == 2:
        msg.set_content(f'{otp} is you otp for password reset\nDont not share with anyone\nThank you Agrirent Team')
        msg['Subject'] = f'OTP for Agrirent password reset'
    try:
        server.starttls()
        server.login('smitkunpara@gmail.com', 'kggxuxcgrxoxfwve')
        server.send_message(msg)
        server.quit()
        return True
    except:
        server.quit()
        return False

def signin(request):
    if request.method == "POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=farmer.objects.filter(email=email,password=password).first()
        if user is not None:
            request.session['currentfarmer']=user.email
            return render(request, 'profile.html',{"name":user.fname,"email":user.email,"dob":user.dob})
        else:
            return render(request, 'authentication/signin.html',{"message":"invalid credentials"})
    return render(request, 'authentication/signin.html')    


def signup(request):
    print(request.method)
    if request.method == "POST":
        fname=request.POST.get('fname')
        dob=request.POST.get('dob')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        if farmer.objects.filter(email=email).exists():
            return render(request, 'authentication/signup.html',{"message":"email is already registered with us"})
        if pass1!=pass2:
            return render(request, 'authentication/signup.html',{"message":"password must be same"})
        otp = random.randint(10000, 99999)
        if send_mail(email, otp, 1):
            request.session['otp'] = otp
            request.session['signup_attempts'] = 0
            request.session['newfarmer']={
                                            'fname': fname,
                                            'dob': dob,
                                            'email': email,
                                            'password': pass1
                                        }
            return redirect('/verify_otp')
        else:
            return render(request, 'authentication/signup.html', {"message": "Invalid email"})
    return render(request, 'authentication/signup.html')


def verify_otp(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        if int(otp) == request.session['otp']:
            try:
                newfarmer = farmer.objects.create(fname=request.session['newfarmer']['fname'],
                                                  dob=request.session['newfarmer']['dob'],
                                                  email=request.session['newfarmer']['email'],
                                                  password=request.session['newfarmer']['password'])
                newfarmer.save()
                request.session['currentfarmer'] = newfarmer[newfarmer.email]
                del request.session['otp']
                del request.session['newfarmer']
                del request.session['signup_attempts']
                return render(request,'profile.html',{"name":newfarmer.fname,"email":newfarmer.email,"dob":newfarmer.dob})
            except IntegrityError:
                messages.error(request, "unable to create account")
                return redirect('signup')
        else:
            request.session['signup_attempts'] += 1
            if request.session['signup_attempts'] == 3:
                del request.session['otp']
                del request.session['newfarmer']
                del request.session['signup_attempts']
                return render(request, 'authentication/signup.html', {"message": "you have exceeded otp attempts"})   
            return render(request, 'authentication/otp.html', {"email": request.session['newfarmer']['email'],
                                                                "message": "Invalid otp"})
    return render(request, 'authentication/otp.html', {"email": request.session['newfarmer']['email']})
def main(request):
    return render(request, 'home.html')