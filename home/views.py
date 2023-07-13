import datetime
from django.shortcuts import render,redirect
from .models import shared_equipment, taken_equipment
from authentication.models import farmer
from django.contrib import messages
import random
import string


def editprofile(request):
    x=verify_request(request)
    if not x==None:
        return x
    print(type(farmer.objects.filter(email=request.session['currentfarmer']).first()))
    if request.method == "POST":
        currentfarmer = farmer.objects.filter(email=request.session['currentfarmer']).first()
        currentfarmer.fname = request.POST.get('name')
        currentfarmer.dob = request.POST.get('dob')
        currentfarmer.pincode = request.POST.get('pincode')
        currentfarmer.address = request.POST.get('address')
        currentfarmer.city = request.POST.get('city')
        currentfarmer.state = request.POST.get('state')
        currentfarmer.contry = request.POST.get('country')
        currentfarmer.village = request.POST.get('village')
        currentfarmer.p_image = request.FILES.get('image')
        currentfarmer.save()
        return redirect('/profile')
    return render(request,'home/editprofile.html',{'f':farmer.objects.filter(email=request.session['currentfarmer']).first()})

def settings(request):
    x=verify_request(request)
    if not x==None:
        return x
    if request.method=="POST":
        currentfarmer = farmer.objects.filter(email=request.session['currentfarmer']).first()
        if 'pass' in request.POST:
            cpass=request.POST.get('pass')
            if cpass==currentfarmer.password:
                currentfarmer.delete()
                messages.success(request,"Account Deleted Successfully")
                return redirect('/signout')
            else:
                messages.error(request,"Incorrect Password")
        else:
            cpass=request.POST.get('cpass')
            if cpass==currentfarmer.password:
                pass1=request.POST.get('pass1')
                pass2=request.POST.get('pass2')
                if pass1==pass2:
                    currentfarmer.password=pass1
                    currentfarmer.save()
                    messages.success(request,"Password Changed Successfully")
                    return redirect('/profile')
                else:
                    messages.error(request,"Both Passwords are not same")
            else:
                messages.error(request,"Incorrect Password")
    return render(request,'home/settings.html')


def chat(request):
    x=verify_request(request)
    if not x==None:
        return x
    if profilecheck(request)==False:
        return redirect('/editprofile')
    return render(request,'home/chat.html')

def myequipment(request):
    x=verify_request(request)
    if not x==None:
        return x
    if is_profile_complete(request)==False:
        messages.error(request,"You need to complete your profile for this feature")
        return redirect(request.META.get('HTTP_REFERER'))
    currentfarmer = farmer.objects.filter(email=request.session['currentfarmer']).first()
    if request.method == "POST":
        which_eq = request.POST.get('equ')
        if which_eq=="shared Equipments":
            return render(request,'home/myeq.html',{'eq':shared_equipment.objects.filter(farmer=currentfarmer), 'which':which_eq})
        elif which_eq=="rented Equipments":
            return render(request,'home/myeq.html',{'eq':taken_equipment.objects.filter(taken_by=currentfarmer), 'which':which_eq})
    return render(request,'home/myeq.html',{'eq':shared_equipment.objects.filter(farmer=currentfarmer)})

def rentequipment(request):
    x=verify_request(request)
    if not x==None:
        return x
    if is_profile_complete(request)==False:
        messages.error(request,"You need to complete your profile for this feature")
        return redirect(request.META.get('HTTP_REFERER'))
    if request.method == "POST":
        if 'equ' in request.POST:
            name = request.POST.get('equ')
            pincode = request.POST.get('pincode')
            print(name, pincode)
            all_equipment = shared_equipment.objects.filter(name=name)
            print(all_equipment)
            return render(request, 'home/renteq.html', {'eq':all_equipment, 'pincode':pincode, 'name':name})
        elif 'uid' in request.POST:
            return redirect('/eid='+request.POST.get('uid'))
    return render(request, 'home/renteq.html', {})

def profile(request):
    x=verify_request(request)
    if not x==None:
        return x
    return render(request, 'home/profile.html', {'farmer':farmer.objects.filter(email=request.session['currentfarmer']).first()})


def shareequipment(request):
    x=verify_request(request)
    if not x==None:
        return x
    if is_profile_complete(request)==False:
        messages.error(request,"You need to complete your profile for this feature")
        return redirect(request.META.get('HTTP_REFERER'))
    if request.method == "POST":
        new_equipment = shared_equipment()
        new_equipment.farmer = farmer.objects.filter(email=request.session['currentfarmer']).first()
        new_equipment.name = str(request.POST.get('equ'))
        new_equipment.uid = generate_equipment_id(20)    
        new_equipment.company = str(request.POST.get('company'))
        new_equipment.model = str(request.POST.get('model'))
        new_equipment.description = str(request.POST.get('discription'))
        new_equipment.price = int(request.POST.get('price'))
        new_equipment.image = request.FILES.get('image')
        new_equipment.pincode = int(request.POST.get('pincode'))
        new_equipment.city = str(request.POST.get('city'))
        new_equipment.state = str(request.POST.get('state'))
        new_equipment.country = str(request.POST.get('country'))
        new_equipment.village = str(request.POST.get('village'))
        new_equipment.mobile = int(request.POST.get('num'))
        new_equipment.no_of_eq= request.POST.get('n_eq')
        new_equipment.address = str(request.POST.get('address'))
        new_equipment.save()
    return render(request, 'home/shareeq.html')

def generate_equipment_id(length):
    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    equipment_id = ''.join(random.choice(characters) for _ in range(length))
    if shared_equipment.objects.filter(uid=equipment_id).exists():
        generate_equipment_id(length)
    return equipment_id

def is_profile_complete(request):
    currentfarmer = farmer.objects.filter(email=request.session['currentfarmer']).first()
    if currentfarmer.pincode == None or currentfarmer.pincode=="":
        return False
    else:
        return True

def equipment_details(request, uid):
    eq = shared_equipment.objects.get(uid=uid)
    return render(request, 'home/product.html', {'eq':eq})
    
def verify_request(request):
    if  not request.session.has_key('currentfarmer'):
        print("inside vefify request")
        request.session['error'] = "Signin to view this page"
        return redirect('/signin')
    else:
        currentdatetime = datetime.datetime.now()
        currentfarmer = farmer.objects.filter(email=request.session['currentfarmer']).first()
        previousdatetime = currentfarmer.last_login.second
        if currentdatetime.second - previousdatetime > 3600:
            del request.session['currentfarmer']
            request.session['error'] = "Session expired, signin again"
            return redirect('/signin')
        else:
            currentfarmer.last_request_time = currentdatetime
            currentfarmer.save()


def signout(request):
    if not request.session.has_key('currentfarmer'):
        return redirect('/')
    del request.session['currentfarmer']
    return redirect('/')