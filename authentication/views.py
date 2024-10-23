from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import IntegrityError
from .models import farmer
import smtplib
from validate_email import validate_email
from email.message import EmailMessage
import random

def forgot_password(request):
    if not request.session.has_key('n'):
        return redirect('/forgotpass')
    if request.method == "POST":
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        otp   = request.POST.get('otp')
        if pass1!=pass2:
            messages.error(request,"Password must be same in both fields")
            return redirect('/forgot_password')
        if int(otp)!=request.session['otp']:
            request.session['n']-=1
            messages.error(request,"Incorrect OTP,You have "+str(request.session['n'])+" attempts left")
            return redirect('/forgot_password')
        else:
            if request.session['n']==0:
                del request.session['email']
                del request.session['otp']  
                del request.session['n']
                messages.error(request,"You have exceeded the number of attempts")
                return redirect('/forgotpass')
            try:
                farmer.objects.filter(email=request.session['email']).update(password=pass1)
                del request.session['email']
                del request.session['otp']
                del request.session['n']
                messages.success(request,"Password Updated Successfully")
                return redirect('/signin')
            except IntegrityError:
                messages.error(request,"Password Updation Failed")
                return redirect('/forgot_password')
    return render(request, 'authentication/forgot_password.html',{"email":request.session['email']})

def pass_forgot_otp(request):
    if request.method=="POST":
        email=request.POST.get('email')
        if email not in farmer.objects.all().values_list('email', flat=True):
            messages.error(request,"Email not registered")
            return redirect('/forgotpass')
        new_otp=random.randint(100000,999999)
        if send_mail(email,new_otp,farmer.objects.get(email=email).fname):
            request.session['email']=email
            request.session['otp']=new_otp
            request.session['n']=3
            messages.success(request,"OTP sent to your email")
            return redirect('/forgot_password')
        else:
            messages.error(request,"OTP sending failed")
            return redirect('/forgotpass')
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
        server.login('team.agrirent@gmail.com', 'opsj fsny pzuu udma')
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
        print(email,password)
        user=farmer.objects.filter(email=email,password=password).first()
        print(user)
        if user is not None:
            request.session['currentfarmer']=user.email
            user.last_login=timezone.now()
            user.save()
            return redirect('/profile/')
        else:
            messages.error(request,"Email or Password is incorrect")
            return redirect('/signin')
    return render(request, 'authentication/signin.html')    


def signup(request):
    if request.method == "POST":
        fname=request.POST.get('fname')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        mobile=request.POST.get('mobile')
        if farmer.objects.filter(email=email).exists():
            messages.error(request,"Email already exists")
            return redirect('/signup')
        if pass1!=pass2:
            messages.error(request,"Passwords must be same")
            return redirect('/signup')
        otp = random.randint(100000, 999999)
        
        if not validate_email(email_address=email, check_format=True, check_blacklist=True, check_dns=True, dns_timeout=10, check_smtp=True, smtp_timeout=10, smtp_helo_host=None, smtp_from_address=None, smtp_debug=False):
            messages.error(request,"Invalid email")
            return redirect('/signup')
        if send_mail(email, otp, fname):
            request.session['otp'] = str(otp)
            request.session['signup_attempts'] = 0
            request.session['newfarmer']={
                "fname":fname,
                "email":email,
                "password":pass1,
                "mobile":mobile,
            
            }
            messages.success(request, "OTP sent to your email")
            return redirect('/verify_otp')
        else:
            messages.error(request,"OTP sending failed")
            return redirect('/signup')
    return render(request, 'authentication/signup.html')


def verify_otp(request):
    if not request.session.has_key('signup_attempts'):
        return redirect('/signup')
    if request.method == "POST":
        otp = request.POST.get('otp')
        print(otp, request.session['otp'])
        if otp == request.session['otp']:
            try:
                newfarmer = farmer(fname=request.session['newfarmer']['fname'],
                                    email=request.session['newfarmer']['email'],
                                    password=request.session['newfarmer']['password'],
                                    mobile=request.session['newfarmer']['mobile'])
                newfarmer.last_login = timezone.now()
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
            messages.error(request, "Invalid OTP,You have " + str(3 - request.session['signup_attempts']) + " attempts left")
            return redirect('/verify_otp')
    return render(request, 'authentication/otp.html', {"email": request.session['newfarmer']['email']})

