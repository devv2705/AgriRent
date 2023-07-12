from django.db import models
from authentication.models import farmer

class shared_equipment(models.Model):
    farmer = models.ForeignKey(farmer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100,blank=True,null=True)
    model = models.CharField(max_length=100,blank=True,null=True)
    uid = models.CharField(max_length=100)
    description = models.CharField(max_length=100,blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='static/home/eqimages')
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    no_of_eq = models.IntegerField()
    mobile = models.IntegerField(blank=True,null=True)
    pincode = models.IntegerField(blank=True,null=True) 
    village = models.CharField(max_length=100,blank=True,null=True)
    city = models.CharField(max_length=100,blank=True,null=True)
    state = models.CharField(max_length=100,blank=True,null=True)
    country = models.CharField(max_length=100,blank=True,null=True)
    address = models.CharField(max_length=100,blank=True,null=True)
    

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Shared Equipment'

class taken_equipment(models.Model):
    taken_by = models.ForeignKey(farmer, on_delete=models.CASCADE,related_name='taken_by')
    taken_from = models.ForeignKey(farmer, on_delete=models.CASCADE,related_name='taken_from')
    def __str__(self):
        return self.taken_by.email
    
    class Meta:
        verbose_name_plural = 'Taken Equipment'
    
