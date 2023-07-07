from django.db import models

# Create your models here.
class farmerdata(models.Model):
    fname=models.CharField(max_length=50)
    email=models.EmailField(max_length=100)
    dob=models.DateField()
    password=models.CharField(max_length=100)
    Created=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    class Meta:
        verbose_name_plural='All farmers data'
    
    