from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from . import models as my_models

COUNTRY_CHOICES = [
    ('india','india'),
    ('bangladesh','bangladesh'),
    ('pakistan','pakistan')
]
STATE_CHOICES =[
('gujarat','gujarat'),
('maharastra','maharastra'),
('rajesthan','rajesthan')
]

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30,widget=forms.TextInput)
    password = forms.CharField(label=("Password"),widget=forms.PasswordInput)


class ProfileForm(forms.Form):
    firstname = forms.CharField(label='First Name', max_length=125,widget=forms.TextInput)
    lastname = forms.CharField(label='Last Name',max_length=125,widget=forms.TextInput)
    mobileno = forms.CharField(label='Mobile No.',max_length=13,widget=forms.TextInput)
    alternamemobile = forms.CharField(label='Alternate Mobile',max_length=13)
    email = forms.CharField(label='Email', disabled=True,required=False)
    addressline1 = forms.CharField(label='Address Line 1',max_length=30)
    addressline2 = forms.CharField(label='Address Line 2',max_length=30)
    city = forms.CharField(label='City',max_length=30,widget=forms.TextInput)
    state = forms.CharField(label='State',max_length=30,widget=forms.TextInput)
    zipcode = forms.CharField(label='Zipcode',max_length=30)
    country = forms.CharField(label='Country',max_length=30,widget=forms.TextInput)

