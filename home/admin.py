from django.contrib import admin
from .models import shared_equipment,taken_equipment


admin.site.register(shared_equipment)
admin.site.register(taken_equipment)