from django.db import models
from authentication.models import farmer

class shared_equipment(models.Model):
    farmer = models.ForeignKey(farmer, on_delete=models.CASCADE)
    equipment = models.CharField(max_length=100)
    equipment_company = models.CharField(max_length=100,blank=True,null=True)
    equipment_model = models.CharField(max_length=100,blank=True,null=True)
    equipment_id = models.CharField(max_length=100)
    equipment_description = models.CharField(max_length=100,blank=True)
    equipment_price = models.IntegerField()
    equipment_image = models.ImageField(upload_to='shared_equipment_image')
    euipment_pincode = models.IntegerField()
    equipment_contact = models.IntegerField()
    equipment_date = models.DateField(auto_now_add=True)
    equipment_time = models.TimeField(auto_now_add=True)
    no_of_equipment = models.IntegerField()

    def __str__(self):
        return self.equipment
    
    class Meta:
        verbose_name_plural = 'Shared Equipment'

class taken_equipment(models.Model):
    taken_by = models.ForeignKey(farmer, on_delete=models.CASCADE,related_name='taken_by')
    taken_from = models.ForeignKey(farmer, on_delete=models.CASCADE,related_name='taken_from')
    def __str__(self):
        return self.taken_equipment
    
    class Meta:
        verbose_name_plural = 'Taken Equipment'
    
