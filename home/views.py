import datetime
from django.shortcuts import render,redirect
from .models import shared_equipment, taken_equipment
from authentication.models import farmer
import random
import string


def editprofile(request):
    verify_request(request)
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
    return render(request,'home/complateProfile.html',{'f':farmer.objects.filter(email=request.session['currentfarmer']).first()})

def settings(request):
    verify_request(request)
    if request.method=="POST":
        currentfarmer = farmer.objects.filter(email=request.session['currentfarmer']).first()
        if request.POST.has_key('delete'):
            currentfarmer.delete()
            #add pop-up here
            return redirect('/logout')
        else:
            cpass=request.POST.get('cpass')
            if cpass==currentfarmer.password:
                pass1=request.POST.get('pass1')
                pass2=request.POST.get('pass2')
                if pass1==pass2:
                    currentfarmer.password=pass1
                    currentfarmer.save()
                    # add pop-up here
                    return redirect('/profile')
                else:
                    return render(request,'home/settings.html',{'message':'password must be same'})
        
    if request.session.has_key('error'):
        error=request.session['error']
        del request.session['error']
        return render(request,'home/settings.html',{'message':error})
            
    return render(request,'home/settings.html')

def chat(request):
    verify_request(request)
    return render(request,'home/chat.html')

def myequipment(request):
    verify_request(request)
    currentfarmer = farmer.objects.filter(email=request.session['currentfarmer']).first()
    if request.method == "POST":
        which_eq = request.POST.get('equ')
        if which_eq=="shared Equipments":
            return render(request,'home/myeq.html',{'eq':shared_equipment.objects.filter(farmer=currentfarmer), 'which':which_eq})
        elif which_eq=="rented Equipments":
            return render(request,'home/myeq.html',{'eq':taken_equipment.objects.filter(taken_by=currentfarmer), 'which':which_eq})
    return render(request,'home/myeq.html',{'eq':shared_equipment.objects.filter(farmer=currentfarmer)})

def search(request):
    verify_request(request)
    if request.method == "POST":
        if 'equ' in request.POST:
            name = request.POST.get('equ')
            pincode = request.POST.get('pincode')
            print(name, pincode)
            all_equipment = shared_equipment.objects.filter(name=name)
            print(all_equipment)
            return render(request, 'home/buy.html', {'eq':all_equipment, 'pincode':pincode, 'name':name})
        elif 'uid' in request.POST:
            return redirect('/eid='+request.POST.get('uid'))
    return render(request, 'home/buy.html', {})

def profile(request):
    verify_request(request)
    return render(request, 'home/user.html', {'farmer':farmer.objects.filter(email=request.session['currentfarmer']).first()})


def shareequipment(request):
    verify_request(request)
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
    return render(request, 'home/sell.html')

def generate_equipment_id(length):
    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    equipment_id = ''.join(random.choice(characters) for _ in range(length))
    if shared_equipment.objects.filter(uid=equipment_id).exists():
        generate_equipment_id(length)
    return equipment_id


def equipment_details(request, uid):
    eq = shared_equipment.objects.get(uid=uid)
    return render(request, 'home/product.html', {'eq':eq})
    
def verify_request(request):
    if not request.session.has_key('currentfarmer'):
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
