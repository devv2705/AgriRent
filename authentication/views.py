from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import IntegrityError
from .models import farmer
import smtplib
from email.message import EmailMessage
import random

def alreadylogin(request):
    if request.session.has_key('currentfarmer'):
        return True
    else:
        return False
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
        if send_mail(email,new_otp,farmer.objects.get(email=email).fname):
            request.session['email']=email
            request.session['otp']=new_otp
            request.session['n']=3
            print(new_otp)
            return redirect('/forgot_password')
        else:
            return render(request, 'authentication/email_for_forgot_password.html',{"message":"error in sending otp\n try again"})
    return render(request,'authentication/email_for_forgot_password.html')
        
def send_mail(email,otp,name):
    server = smtplib.SMTP('smtp.gmail.com', '587')
    msg = EmailMessage()
    msg['Subject'] = "OTP verification"
    msg['From'] = "team.agrirent@gmail.com"
    msg['To'] = email
    html_content = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        /* Global styles */
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }

        /* Container styles */
        .container {
            max-width: 500px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Box styles */
        .box {
            border: 1px solid #CCCCCC;
            border-radius: 6px;
            padding: 20px;
            margin-bottom: 20px;
        }

        /* OTP styles */
        .otp {
            font-size: 24px;
            font-weight: bold;
            margin: 0;
        }

        /* Warning styles */
        .warning {
            color: red;
            font-size: 12px;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <!-- Email container -->
    <div class="container">
        <!-- Box with OTP -->
        <div class="box">
            <p>Dear '''+name+''',</p>
            <p>Here is your OTP:</p>
            <p class="otp">'''+str(otp)+'''</p>
        </div>

        <!-- Warning not to share OTP -->
        <p class="warning"><strong>Warning:</strong> Do not share this OTP with anyone.</p>
    </div>
</body>
</html>
'''
    msg.add_alternative(html_content, subtype='html')
    try:
        server.starttls()
        server.login('team.agrirent@gmail.com', 'easjciiobhlwfhjy')
        server.send_message(msg)
        server.quit()
        return True
    except:
        server.quit()
        return False

def signin(request):
    if alreadylogin(request):
        return redirect('/profile/')
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
            user.last_login=timezone.now()
            return redirect('/profile/')
        else:
            return render(request, 'authentication/signin.html',{"message":"invalid credentials"})
    return render(request, 'authentication/signin.html')    


def signup(request):
    if alreadylogin(request):
        return redirect('/profile/')
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
        if send_mail(email, otp, fname):
            request.session['otp'] = str(otp)
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
        if otp == request.session['otp']:
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

