

from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import *
from account .models import *




class LoanRequestForm(forms.ModelForm):
    class Meta:
        model = loanRequest
        fields = ('category', 'amount','guarantor_name','guarantor_no' )


class LoanTransactionForm(forms.ModelForm):
    class Meta:
        model =loanTransaction
        fields = ('payment',)









class CustomerBankForm(ModelForm):
    class Meta:
        model = CustomerBank
        fields =('bank_name', 'account_no','next_of_kin' )
        Widget ={
             'bank_name':forms.TextInput(attrs={'class':'form-control'}),
            'account_no':forms.TextInput( attrs={'class':'form-control'}),

           # 'nin':forms.TextInput(attrs={'class':'form-control'}),
           # 'bvn':forms.TextInput(attrs={'class':'form-control'}),
           # 'card_no':forms.TextInput(attrs={'class':'form-control'}),
            'next_of_kin':forms.TextInput(attrs={'class':'form-control'}),
           
        }
 



class UpdateCustomerBankForm(ModelForm):
    class Meta:
        model = CustomerBank
        fields =('bank_name', 'account_no','next_of_kin' )
       