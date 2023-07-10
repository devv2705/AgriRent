from django.shortcuts import render
from .models import shared_equipment, taken_equipment
from django.db.models import F
import random
import string


def home(request):
    return render(request, 'home.html', {})

def search(request):
    if request.method == "POST":
        equipment = request.POST.get('equipment')
        equipment_pincode = request.POST.get('equipment_pincode')
        all_equipment = shared_equipment.objects.filter(equipment=equipment, equipment_pincode=equipment_pincode)
        # Calculate the absolute difference between the provided pincode and equipment_pincode
        all_equipment = shared_equipment.objects.annotate(pincode_difference=Abs(F('equipment_pincode') - equipment_pincode))
        # Filter based on equipment type and sort by pincode difference in ascending order
        all_equipment = all_equipment.filter(equipment=equipment).order_by('pincode_difference')
        return render(request, 'search.html', {'all_equipment':all_equipment})
    return render(request, 'search.html', {})

# def rentequipment(request):
#     return render(request, 'rentequipment.html', {})

def shareequipment(request):
    if request.method == "POST":
        new_equipment = shared_equipment()
        new_equipment.farmer = request.POST.get('farmer')
        new_equipment.equipment = request.POST.get('equipment')
        new_equipment.equipment_id = generate_equipment_id(20)    
        new_equipment.equipment_company = request.POST.get('equipment_company')
        new_equipment.equipment_model = request.POST.get('equipment_model')
        new_equipment.equipment_description = request.POST.get('equipment_description')
        new_equipment.equipment_price = request.POST.get('equipment_price')
        new_equipment.equipment_image = request.POST.get('equipment_image')
        new_equipment.equipment_location = request.POST.get('equipment_location')
        new_equipment.equipment_contact = request.POST.get('equipment_contact')
        new_equipment.equipment_date = request.POST.get('equipment_date')
        new_equipment.equipment_time = request.POST.get('equipment_time')
        new_equipment.no_of_equipment = request.POST.get('no_of_equipment')
        new_equipment.save()

    return render(request, 'shareequipment.html', {})

def generate_equipment_id(length):
    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
    equipment_id = ''.join(random.choice(characters) for _ in range(length))
    if shared_equipment.objects.filter(equipment_id=equipment_id).exists():
        generate_equipment_id(length)
    return equipment_id

  
def equipment_details(request, equipment_id):
    equipment = shared_equipment.objects.get(equipment_id=equipment_id)
    return render(request, 'equipment_details.html', {'equipment':equipment})