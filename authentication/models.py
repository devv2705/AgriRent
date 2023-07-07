from django.db import models

# Create your models here.
class usersdata(models.Model):
    email=models.EmailField(max_length=100)
    aadharnumber=models.CharField(max_length=12)
    password=models.CharField(max_length=100)
    Created=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    class Meta:
        verbose_name_plural='All Users Data'
    
    