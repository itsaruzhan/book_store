from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from phonenumber_field.modelfields import PhoneNumberField

from django import forms


class NewUserForm(UserCreationForm):
    GENDER = [
        ('M',  'Male') , 
        ('F',  'Female')
    ]
    
    email = forms.EmailField()
    phoneNumber = PhoneNumberField(null = False, blank = False).formfield()
    gender = forms.ChoiceField(choices=GENDER)


    class Meta:
        model = User
        fields = ("first_name","last_name","username",  "email", "phoneNumber", "gender", "password1", "password2")
        
