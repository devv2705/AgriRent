from django.shortcuts import render
from .models import shared_equipment, taken_equipment
# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def search(request):
    if request.method == "POST":
        equipment = request.POST.get('equipment')
        equipment_pincode = request.POST.get('equipment_pincode')
        equipment_min_price = request.POST.get('equipment_min_price')
        equipment_max_price = request.POST.get('equipment_max_price')
        
        all_equipment = shared_equipment.objects.filter(equipment=equipment, equipment_pincode=equipment_pincode, equipment_price__gte=equipment_min_price, equipment_price__lte=equipment_max_price)
        
    return render(request, 'search.html', {})

def rentequipment(request):
    return render(request, 'rentequipment.html', {})

def shareequipment(request):
    if request.method == "POST":
        new_equipment = shared_equipment()
        new_equipment.farmer = request.POST.get('farmer')
        new_equipment.equipment = request.POST.get('equipment')
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

