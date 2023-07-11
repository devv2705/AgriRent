from django.db import models

# Create your models here.
class farmer(models.Model):
    fname=models.CharField(max_length=50)
    email=models.EmailField(max_length=100)
    dob=models.CharField(max_length=10)
    password=models.CharField(max_length=100)
    otp_chance=models.IntegerField(default=3)
    Created=models.DateTimeField(auto_now_add=True)
    pincode = models.IntegerField(blank=True,null=True)
    village = models.CharField(max_length=100,blank=True)
    mobile = models.IntegerField(blank=True,null=True)
    
    
    def __str__(self):
        return self.email
    class Meta:
        verbose_name_plural='All farmers data'
    
    