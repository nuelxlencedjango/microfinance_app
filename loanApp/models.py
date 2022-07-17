from operator import truediv
from django.db import models
from django.contrib.auth.models import User
from account.models import *
#from utils import create_new_ref_number
import random
import uuid
# Create your models here.




class CustomerBank(models.Model):
    user = models.OneToOneField(User,null=True,blank=True, on_delete= models.SET_NULL,related_name='customer_bank')

    bank_name =models.CharField(max_length=250,null=True,blank=True)
    account_no = models.CharField(max_length=14, null=True,blank=True,unique=True)
    nin  = models.CharField(max_length=11, null=True,blank=True,unique=True)
    bvn  = models.CharField(max_length=11, null=True,blank=True,unique=True)
    card_no = models.CharField(max_length=50, null=True,blank=True,unique=True)
    next_of_kin = models.CharField(max_length=200, null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.user)




class loanCategory(models.Model):
    loan_type = models.CharField(max_length=250)
    #date_requested = models.DateField(auto_now_add=True)
    date_approved =  models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.loan_type


class loanRequest(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_loan')
    category = models.ForeignKey(loanCategory, on_delete=models.CASCADE, null=True)
    request_date = models.DateField(auto_now_add=True)
    status_date = models.CharField(max_length=150, null=True, blank=True, default=None)
    guarantor_name = models.CharField(max_length=100, null=True,blank=True)
    guarantor_no = models.CharField(max_length=15, null=True,blank=True)
    #reason = models.TextField()
    status = models.CharField(max_length=100, default='pending')
    amount = models.PositiveIntegerField(default=1000)
    days = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.customer.username


    def interestRate(self):
        interest = (self.amount*10)/100
        totalAmount = interest + self.amount
        return totalAmount


               


class CustomerLoan(models.Model):
    customer = models.ForeignKey(User,null=True,  on_delete=models.CASCADE, related_name='loan_user')
    total_loan = models.PositiveIntegerField(default=0)
    payable_loan = models.PositiveIntegerField(default=0)
    date_approved =  models.DateTimeField(auto_now=True)

   #def get_final_amount(self):
      #return (self.get_total_price() + self.get_vat())

    def __str__(self):
        return self.customer.username

    




class loanTransaction(models.Model):
    customer = models.ForeignKey(User,null=True, on_delete=models.CASCADE, related_name='transaction_customer')

    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False,null=True)
    #transaction_id = models.CharField(max_length=36, default=uuid.uuid4,editable=True)
   # payment_id =models.CharField(max_length=50,unique=True, default =None,blank=True,null=True)

    payment = models.PositiveIntegerField(default=0)
    payment_date = models.DateField(auto_now_add=True)
    balance =models.PositiveIntegerField(default=0)


  
   

    def __str__(self):
        return self.customer.first_name

     

   

      

    #class Transaction(models.Model):
       # Referrence_Number = models.Charfield( max_length = 10,blank=True,editable=False,unique=True,default=create_new_ref_number )

    #def create_new_ref_number():
              #  not_unique = True
               # while not_unique:
#unique_ref = random.randint(1000000000, 9999999999)
                  #  if not Transaction.objects.filter(Referrence_Number=unique_ref):
                   #     not_unique = False
               # return str(unique_ref)
  

class Repayment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loan_repayment')
  
    initialAmount = models.ForeignKey(CustomerLoan, on_delete=models.CASCADE, null=True)   
    payment = models.PositiveIntegerField(default=0)   
