from django import forms
from .models import usersdata

class loginform(forms.Form):
    email=forms.EmailField(max_length=100)
    password=forms.PasswordInput()