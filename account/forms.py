
from dataclasses import fields
#from tkinter import Widget
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import *


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        #fields ="__all__"
        fields = ('username', 'email', 'password1', 'password2','first_name','last_name')



class CustomerInfoForm(ModelForm):
    class Meta:
        model = CustomerInfo
        fields =('address','nearest_bustop','business','location','profile_img','phone','state') 
        Widget ={
             'phone':forms.TextInput(attrs={'class':'form-control'}),
            'profile_img':forms.TextInput( attrs={'class':'form-control'}),

            'address':forms.TextInput(attrs={'class':'form-control'}),
            'nearest_bustop':forms.TextInput(attrs={'class':'form-control'}),
            'location':forms.NumberInput(attrs={'class':'form-control'}),
            'business':forms.TextInput(attrs={'class':'form-control'}),
           
        }
    def __init__(self ,*args ,**kwargs):

        super(CustomerInfoForm,self).__init__(*args ,**kwargs)
        self.fields['location'].empty_label ="select location"

        super(CustomerInfoForm,self).__init__(*args ,**kwargs)
        self.fields['state'].empty_label ="select state"




class UserUpdateForm(forms.ModelForm):
  class Meta:

    model = User
    fields =('username' ,'email')



class UserUpdatePasswordForm(forms.ModelForm):

  class Meta:
    model = User
    fields =('password','username')



class CustomerLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')



class UpdateCustomerForm(forms.ModelForm):
    information = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = CustomerInfo
        exclude = ['user']
