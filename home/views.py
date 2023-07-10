from django.shortcuts import render,redirect
from .models import shared_equipment, taken_equipment
from authentication.models import farmer
from django.db.models import F
from django.db.models.functions import Abs
import random
import string

def search(request):
    if not request.session.has_key('currentfarmer'):
        return redirect('/signin')
    if request.method == "POST":
        if 'equ' in request.POST:
            name = request.POST.get('equ')
            pincode = request.POST.get('pincode')
            print(name, pincode)
            all_equipment = shared_equipment.objects.filter(equipment=name)
            return render(request, 'home/buy.html', {'eq':all_equipment})
        elif 'equipment_id' in request.POST:
            return redirect('/eid='+request.POST.get('equipment_id'))
    return render(request, 'home/buy.html', {})

def takenequipment(request):
    if not request.session.has_key('currentfarmer'):
        return redirect('/signin')
    new_equipment = taken_equipment()
    myeq = taken_equipment.objects.filter(taken_by=request.session['currentfarmer'])
    return render(request, 'home/takenequipment.html', {'myeq':myeq})


def shareequipment(request):
    if not request.session.has_key('currentfarmer'):
        return redirect('/signin')
    if request.method == "POST":
        new_equipment = shared_equipment()
        new_equipment.farmer = farmer.objects.filter(email=request.session['currentfarmer']).first()
        # print(request.session['currentfarmer'])
        new_equipment.equipment = str(request.POST.get('equ'))
        new_equipment.equipment_id = generate_equipment_id(20)    
        new_equipment.equipment_company = str(request.POST.get('company'))
        new_equipment.equipment_model = str(request.POST.get('model'))
        new_equipment.equipment_description = str(request.POST.get('discription'))
        new_equipment.equipment_price = int(request.POST.get('price'))
        new_equipment.equipment_image = request.FILES.get('image')
        new_equipment.euipment_pincode = request.POST.get('pincode')
        new_equipment.equipment_contact = request.POST.get('num')
        new_equipment.no_of_equipment = request.POST.get('n_eq')
        # print(type(request.POST.get('equ')),request.POST.get('equ'))
        # print(type(request.POST.get('company')),request.POST.get('company'))
        # print(type(request.POST.get('model')),request.POST.get('model'))
        # print(type(request.POST.get('discription')),request.POST.get('discription'))
        # print(type(request.POST.get('price')),request.POST.get('price'))
        # print(type(request.POST.get('image')),request.POST.get('image'))
        # print(type(request.POST.get('pincode')),request.POST.get('pincode'))
        # print(type(request.POST.get('num')),request.POST.get('num'))
        # print(type(request.POST.get('n_eq')),request.POST.get('n_eq'))
        # print(type(new_equipment),new_equipment.__dict__)
        new_equipment.save()
    return render(request, 'home/sell.html')

def generate_equipment_id(length):
    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
    equipment_id = ''.join(random.choice(characters) for _ in range(length))
    if shared_equipment.objects.filter(equipment_id=equipment_id).exists():
        generate_equipment_id(length)
    return equipment_id

def equipment_details(request, equipment_id):
    eq = shared_equipment.objects.get(equipment_id=equipment_id)
    return render(request, 'home/product.html', {'eq':eq})


def signout(request):
    if not request.session.has_key('currentfarmer'):
        return render(request, 'main.html', {})
    del request.session['currentfarmer']
    return redirect('/signin')
