from dataclasses import replace
from operator import truediv
from pyexpat.errors import messages
from django.db import models
from django.contrib.auth.models import User
from account.models import *
from django.db.models import Sum
from uuid import uuid4
from django.utils import timezone
from datetime import datetime, timedelta, tzinfo


import uuid





class CustomerBank(models.Model):
    user = models.OneToOneField(User,null=True,blank=True, on_delete= models.SET_NULL,related_name='customer_bank')

    bank_name =models.CharField(max_length=250,null=True,blank=True)
    account_no = models.CharField(max_length=14, null=True,blank=True,unique=True)
    card_no = models.CharField(max_length=50, null=True,blank=True,unique=True)
    next_of_kin = models.CharField(max_length=200, null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.user)



class loanCategory(models.Model):
    loan_type = models.CharField(max_length=250)
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
    balance = models.PositiveIntegerField(default=0)
    payment = models.CharField(max_length=20, default='Not paid yet')
    total_amount_paid = models.PositiveIntegerField(default=0)
    bal = models.PositiveIntegerField(default=0)
    mydate = models.DateTimeField(editable=False,null=True)

    def __str__(self):
        return self.customer.username


    def save(self):
        from datetime import datetime, timedelta
        due_date = timedelta(days=30)
        if not self.id:
            self.mydate = datetime.now() + due_date
            super(CustomerLoan, self).save()   
            

    def get_date(self):
        from .tasks import check_due_date
        check_due_date()         

        


class MyModel(models.Model):
    mydate = models.DateTimeField(editable=False)

    def save(self):
       from datetime import datetime, timedelta
       d = timedelta(days=30)

    # only add 30 days if it's the first time the model is saved
       if not self.id:
        self.mydate = datetime.now() + d
        super(MyModel, self).save()  




class loanTransaction(models.Model):
    customer = models.ForeignKey(User,null=True, on_delete=models.CASCADE, related_name='transaction_customer')

    #transaction_id = models.UUIDField(default=uuid.uuid4, editable=False,null=True)
    transactionId = models.CharField(max_length=200, null=True,blank=True)
    payment = models.PositiveIntegerField(default=0)
    payment_date = models.DateField(blank=True, null=True)
    balance =models.PositiveIntegerField(default=0)
    total_payment =models.PositiveIntegerField(default=0)
     
    def __str__(self):
        return self.customer.username

    
    class Meta:
      verbose_name_plural='loanTransaction'    

    #update customer's transaction
    def updateBalance(self):      
        totalPayable = CustomerLoan.objects.filter(customer=self.customer).aggregate(
        Sum('payable_loan'))['payable_loan__sum']

        totalPaid = loanTransaction.objects.filter(customer=self.customer).aggregate(Sum('payment'))[
        'payment__sum'] 
        bal = totalPayable - totalPaid
        CustomerLoan.objects.filter(customer=self.customer).update(total_amount_paid=totalPaid,balance=bal)


    # generating transaction id and time
    def save(self, *args, **kwargs):
        if self.payment_date is None:
            self.payment_date = timezone.localtime(timezone.now())

            if self.transactionId is None:
                self.transactionId = str(uuid4()).split('-')[4]
   
            super(loanTransaction, self).save(*args, **kwargs)  
  
       

       

