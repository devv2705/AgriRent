import datetime
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import IntegrityError
from .models import farmer
import smtplib
from email.message import EmailMessage
import random

def forgot_password(request):
    if request.session.has_key('error'):
        message=request.session['error']
        del request.session['error']
        return render(request, 'authentication/forgot_password.html',{"message":message,"email":request.session['email']})
    if request.method == "POST":
        print('third')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        otp   = request.POST.get('otp')
        if pass1!=pass2:
            return render(request, 'authentication/forgot_password.html',{"message":"password must be same","email":request.session['email']})
        if int(otp)!=request.session['otp']:
            request.session['n']-=1
            return render(request, 'authentication/forgot_password.html',{"message":"wrong otp","email":request.session['email']})
        else:
            print('sixth')
            if request.session['n']==0:
                request.session['error']='you have reached maximum limit of otp verification'
                return redirect('/forgot_password')
            try:
                print('eighth')
                farmer.objects.filter(email=request.session['email']).update(password=pass1)
                del request.session['email']
                del request.session['otp']
                del request.session['n']
                return redirect('/signin')
            except IntegrityError:
                return render(request, 'authentication/signup.html',{"message":"error in updating password"})
    return render(request, 'authentication/forgot_password.html',{"email":request.session['email']})

def pass_forgot_otp(request):
    if request.session.has_key('error'):
        message=request.session['error']
        del request.session['error']
        return render(request, 'authentication/forgot_password.html',{"message":message})
    if request.method=="POST":
        email=request.POST.get('email')
        if email not in farmer.objects.all().values_list('email', flat=True):
            return render(request, 'authentication/email_for_forgot_password.html',{"message":"email not found"})
        new_otp=random.randint(100000,999999)
        if send_mail(email,new_otp,2):
            request.session['email']=email
            request.session['otp']=new_otp
            request.session['n']=3
            print(new_otp)
            return redirect('/forgot_password')
        else:
            return render(request, 'authentication/email_for_forgot_password.html',{"message":"error in sending otp\n try again"})
    return render(request,'authentication/email_for_forgot_password.html')
        
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
    if request.session.has_key('error'):
        error=request.session['error']
        del request.session['error']
        return render(request, 'authentication/signin.html',{"message":error})
    if request.method == "POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=farmer.objects.filter(email=email,password=password).first()
        if user is not None:
            request.session['currentfarmer']=user.email
            user.last_login=datetime.datetime.now()
            return redirect('/profile/')
        else:
            return render(request, 'authentication/signin.html',{"message":"invalid credentials"})
    return render(request, 'authentication/signin.html')    


def signup(request):
    if request.session.has_key('error'):
        error=request.session['error']
        del request.session['error']
        return render(request, 'authentication/signup.html',{"message":error})
    print(request.method)
    if request.method == "POST":
        fname=request.POST.get('fname')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        mobile=request.POST.get('mobile')
        if farmer.objects.filter(email=email).exists():
            return render(request, 'authentication/signup.html',{"message":"email is already registered with us"})
        if pass1!=pass2:
            return render(request, 'authentication/signup.html',{"message":"password must be same"})
        otp = random.randint(100000, 999999)
        if send_mail(email, otp, 1):
            request.session['otp'] = otp
            request.session['signup_attempts'] = 0
            request.session['newfarmer']={
                "fname":fname,
                "email":email,
                "password":pass1,
                "mobile":mobile,
            
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
                newfarmer = farmer(fname=request.session['newfarmer']['fname'],
                                    email=request.session['newfarmer']['email'],
                                    password=request.session['newfarmer']['password'],
                                    mobile=request.session['newfarmer']['mobile'])
                newfarmer.last_login = datetime.datetime.now()
                newfarmer.p_image = "/static/images/default.jpg"
                newfarmer.save()
                request.session['currentfarmer'] = newfarmer.email
                del request.session['otp']
                del request.session['newfarmer']
                del request.session['signup_attempts']
                
                return redirect('/profile/')
            except IntegrityError:
                messages.error(request, "unable to create account")
                return redirect('/signup')
        else:
            request.session['signup_attempts'] += 1
            if request.session['signup_attempts'] == 3:
                del request.session['otp']
                del request.session['newfarmer']
                del request.session['signup_attempts']
                return render(request, 'authentication/signup.html', {"message": "you have exceeded otp attempts"})   
            return render(request, 'authentication/otp.html', {"email": request.session['newfarmer']['email'],
                                                                "message": "You are left with " + str(3 - request.session['signup_attempts']) + " attempts"})
    return render(request, 'authentication/otp.html', {"email": request.session['newfarmer']['email']})

