from django.utils import timezone
from django.shortcuts import render,redirect,get_object_or_404
from .models import shared_equipment, taken_equipment,Message
from authentication.models import farmer
from django.contrib import messages
from django.db.models import Q

import random
import string

def editprofile(request):
    x=verify_request(request)
    if not x==None:
        return x
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
        messages.success(request,"Profile Updated Successfully")
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
    if is_profile_complete(request)==False:
        messages.error(request,"You need to complete your profile for this feature")
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
        if 'equ' in request.POST:
            which_eq = request.POST.get('equ')
            if which_eq=="shared Equipments":
                return render(request,'home/myeq.html',{'eq':shared_equipment.objects.filter(farmer=currentfarmer), 'which':which_eq})
            elif which_eq=="rented Equipments":
                return render(request,'home/myeq.html',{'eq':taken_equipment.objects.filter(taken_by=currentfarmer), 'which':which_eq})
        else:
            uid=request.POST.get('uid')
            shared_equipment.objects.filter(uid=uid).delete()
    return render(request,'home/myeq.html')

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def get_coordinates(pincode):
    geolocator = Nominatim(user_agent="pincode_locator")
    location = geolocator.geocode(str(pincode))
    if location:
        return location.latitude, location.longitude
    return None, None

def rentequipment(request):
    x = verify_request(request)
    if not x == None:
        return x
    if is_profile_complete(request) == False:
        messages.error(request, "You need to complete your profile for this feature")
        return redirect(request.META.get('HTTP_REFERER'))
    if request.method == "POST":
        if 'equ' in request.POST:
            name = request.POST.get('equ')
            pincode = request.POST.get('pincode')
            given_coordinates = get_coordinates(pincode)

            if given_coordinates[0] is None or given_coordinates[1] is None:
                messages.error(request, "Invalid pincode. Please enter a valid pincode.")
                return redirect(request.META.get('HTTP_REFERER'))

            all_equipment = shared_equipment.objects.exclude(farmer=farmer.objects.filter(email=request.session['currentfarmer']).first())

            # Calculate distances and sort the equipment based on proximity
            sorted_equipment = sorted(all_equipment, key=lambda equipment: geodesic(given_coordinates, get_coordinates(equipment.pincode)).miles)

            return render(request, 'home/renteq.html', {'eq': sorted_equipment, 'pincode': pincode, 'name': name})
        elif 'uid' in request.POST:
            return redirect('/eid=' + request.POST.get('uid'))
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
        messages.success(request,"Equipment Shared Successfully")
        return redirect('/shareeq')
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
    if request.method == "POST":
        if 'edit' in request.POST:
            return render(request, 'home/editeq.html', {'eeq':eq})
        elif 'delete' in request.POST:
            eq.delete()
            messages.success(request,"Equipment Deleted Successfully")
            return redirect('/myeq')
    return render(request, 'home/product.html', {'eq':eq})
    

def verify_request(request):
    if not request.session.has_key('currentfarmer'):
        messages.error(request,"Session Expired, Login Again")
        return redirect('/signin')
    else:
        currentfarmer = farmer.objects.filter(email=request.session['currentfarmer']).first()
        if currentfarmer.last_login is not None:
            if (timezone.now() - currentfarmer.last_login).total_seconds() > 3600*3:
                del request.session['currentfarmer']
                messages.error(request,"Session Expired, Login Again")
                return redirect('/signin')
            else:
                currentfarmer.last_login = timezone.now()
                currentfarmer.save()
        else:
            currentfarmer.last_login = timezone.now()
            currentfarmer.save()
        return None

def signout(request):
    if not request.session.has_key('currentfarmer'):
        return redirect('/')
    del request.session['currentfarmer']
    return redirect('/')


def send_message(request, receiver_id, equipment_id):
    if request.method == 'POST':
        content = request.POST.get('content')  # Get the message content from the form
        if content:  # Check if content is not empty
            sender = farmer.objects.filter(email=request.session['currentfarmer']).first()  # Get the logged-in farmer
            receiver = get_object_or_404(farmer, id=receiver_id)  # Get the receiver
            equipment = get_object_or_404(shared_equipment, uid=equipment_id)  # Ensure you're using uid if that's what you're passing

            # Create a new message
            Message.objects.create(sender=sender, receiver=receiver, equipment=equipment, content=content)
            messages.success(request, "Message sent successfully!")
            return redirect('inbox')  # Redirect to the inbox after sending
        else:
            messages.error(request, "Message content cannot be empty.")
            return redirect(request.META.get('HTTP_REFERER'))  # Redirect back to the previous page

    return redirect('home')  # Redirect to the home page if it's not a POST request

def inbox(request):
    x = verify_request(request)
    if x is not None:
        return x
    
    currentfarmer = farmer.objects.filter(email=request.session['currentfarmer']).first()
    received_messages = Message.objects.filter(receiver=currentfarmer).order_by('-timestamp')
    
    return render(request, 'home/inbox.html', {'messages': received_messages})


def chat_with_owner(request, owner_id, equipment_id):
    x = verify_request(request)
    if not x == None:
        return x

    if is_profile_complete(request) == False:
        messages.error(request, "You need to complete your profile for this feature")
        return redirect('/editprofile')

    current_farmer = farmer.objects.filter(email=request.session['currentfarmer']).first()
    owner = get_object_or_404(farmer, id=owner_id)
    equipment = get_object_or_404(shared_equipment, id=equipment_id)

    # Check if it's a POST request to send a message
    if request.method == "POST":
        message_content = request.POST.get('message')
        if message_content:
            Message.objects.create(sender=current_farmer, receiver=owner, content=message_content, equipment=equipment)
            messages.success(request, "Message sent successfully!")
            return redirect('inbox')

    # Fetch previous chat messages between current farmer and owner for this equipment
    chat_messages = Message.objects.filter(
        (Q(sender=current_farmer, receiver=owner) | Q(sender=owner, receiver=current_farmer)) & Q(equipment=equipment)
    ).order_by('timestamp')

    return render(request, 'home/chat.html', {
        'owner': owner,
        'equipment': equipment,
        'chat_messages': chat_messages,
    })
