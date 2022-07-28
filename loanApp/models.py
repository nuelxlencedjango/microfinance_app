from operator import truediv
from pyexpat.errors import messages
from django.db import models
from django.contrib.auth.models import User
from account.models import *
from django.db.models import Sum
from datetime import datetime, timedelta

#from utils import create_new_ref_number
import random
import uuid
# Create your models here.




class CustomerBank(models.Model):
    user = models.OneToOneField(User,null=True,blank=True, on_delete= models.SET_NULL,related_name='customer_bank')

    bank_name =models.CharField(max_length=250,null=True,blank=True)
    account_no = models.CharField(max_length=14, null=True,blank=True,unique=True)
    #nin  = models.CharField(max_length=11, null=True,blank=True,unique=True)
    #bvn  = models.CharField(max_length=11, null=True,blank=True,unique=True)
    #account_type = models.CharField(max_length=50, null=True,blank=True,unique=True)
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

    total_payment =models.PositiveIntegerField(default=0)
    complete_payment  = models.BooleanField(default=False)
    profit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.customer.username

    def get_total_price(self):
        balance=self.total_payment - self.amount 
        loanRequest.objects.filter(customer=self.customer).update(profit=balance) 

        return balance  





class CustomerLoan(models.Model):
    customer = models.ForeignKey(User,null=True,  on_delete=models.SET_NULL, related_name='loan_user')
    total_loan = models.PositiveIntegerField(default=0)
    payable_loan = models.PositiveIntegerField(default=0)
    date_approved =  models.DateField(auto_now=True)
    #date_approved =  models.DateTimeField(auto_now=True)
    balance = models.PositiveIntegerField(default=0)
    payment = models.CharField(max_length=20, default='Not paid yet')
    total_amount_paid = models.PositiveIntegerField(default=0)

    mydate = models.DateTimeField(editable=False,null=True)

    def __str__(self):
        return self.customer.username


    def save(self):
        from datetime import datetime, timedelta
        due_date = timedelta(days=1)

        # only add 30 days if it's the first time the model is saved
        if not self.id:
            self.mydate = datetime.now() + due_date
            super(CustomerLoan, self).save()    

    
    def get_date(self):
        totalPayable = CustomerLoan.objects.filter(customer=self.customer).aggregate(
        Sum('payable_loan'))['payable_loan__sum']

        totalPaid = loanTransaction.objects.filter(customer=self.customer).aggregate(Sum('payment'))[
        'payment__sum']
        
        if self.mydate ==  datetime.now():
            if totalPayable > totalPaid:
                new_bal =totalPayable - totalPaid

                new_bal =totalPayable + (new_bal *10) / 100
                mydate = datetime.now() + timedelta(days=1)

                CustomerLoan.objects.filter( customer=self.customer).update(mydate=mydate,payable_loan=int(new_bal),bal=int(new_bal)) 

        else:
           
            mydate = datetime.now() + timedelta(days=7)
           
        return 'Please on or before {} '.format(mydate)
        



class MyModel(models.Model):
    mydate = models.DateTimeField(editable=False) # editable=False to hide in admin

    def save(self):
       from datetime import datetime, timedelta
       d = timedelta(days=30)

    # only add 30 days if it's the first time the model is saved
       if not self.id:
        self.mydate = datetime.now() + d
        super(MyModel, self).save()  






    




class loanTransaction(models.Model):
    customer = models.ForeignKey(User,null=True, on_delete=models.CASCADE, related_name='transaction_customer')

    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False,null=True)
    #transaction_id = models.CharField(max_length=36, default=uuid.uuid4,editable=True)
   # payment_id =models.CharField(max_length=50,unique=True, default =None,blank=True,null=True)

    payment = models.PositiveIntegerField(default=0)
    payment_date = models.DateField(auto_now_add=True)
    balance =models.PositiveIntegerField(default=0)

    total_payment =models.PositiveIntegerField(default=0)
     

    def __str__(self):
        return self.customer.username


    def updateBalance(self):
        
        totalPayable = CustomerLoan.objects.filter(customer=self.customer).aggregate(
        Sum('payable_loan'))['payable_loan__sum']

        totalPaid = loanTransaction.objects.filter(customer=self.customer).aggregate(Sum('payment'))[
        'payment__sum'] 
        bal = totalPayable - totalPaid
        CustomerLoan.objects.filter(customer=self.customer).update(total_amount_paid=totalPaid,balance=bal)



    class Meta:
      verbose_name_plural='loanTransaction'
       
    
       







def get_deadline():

    return datetime.today() + timedelta(days=30)

class Bill(models.Model):
    name = models.CharField(max_length=50)
    customer = models.ForeignKey(User, related_name='bills',null=True, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.today)
    deadline = models.DateField(default=get_deadline)  



      

   
