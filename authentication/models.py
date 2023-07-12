from django.db import models

# Create your models here.
class farmer(models.Model):
    fname=models.CharField(max_length=50)
    email=models.EmailField(max_length=100)
    dob=models.CharField(max_length=10)
    password=models.CharField(max_length=100)
    Created=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now=True)
    pincode = models.IntegerField(blank=True,null=True)
    city = models.CharField(max_length=100,blank=True)
    state = models.CharField(max_length=100,blank=True)
    contry = models.CharField(max_length=100,blank=True)
    village = models.CharField(max_length=100,blank=True)
    mobile = models.IntegerField(blank=True,null=True)
    address = models.CharField(max_length=100,blank=True)
    p_image = models.ImageField(upload_to='static/home/pimages',blank=True)

    def __str__(self):
        return self.email
    class Meta:
        verbose_name_plural='All farmers data'
    
    