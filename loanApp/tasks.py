from celery import shared_task
from loanApp.models import CustomerLoan
from django.db.models import Sum
from datetime import datetime, timedelta


#from time import sleep
#from django.core.mail import send_mai


#from celery.utils.log import get_task_logger


#logger = get_task_logger(__name__)


#@shared_task
#def sample_task():
 #   logger.info("The sample task just ran.")

import time



@shared_task
def send_email(email):
    print('A simple message is sent to {email}')    





#def check_due_date(customer,loan,payable_amount,balance,total_amount_paid,date_approved,mydate):
@shared_task
def check_due_date():
    all_customer =CustomerLoan.objects.all()
    for name in all_customer:
        if int(datetime.now().strftime("%s")) <= int(name.mydate.strftime("%s")):
            customer = CustomerLoan.objects.filter(customer=name.customer)#,payable_loan=name.payable_loan)
            for amt in customer:
                amount = amt.payable_loan
                amt_paid = amt.total_amount_paid
            
                if int(amount) > int(amt_paid):
                    new_bal =amount - amt_paid

                    new_bal = (new_bal *10) / 100
                    mydate = datetime.now() + timedelta(days=1)

                    CustomerLoan.objects.filter(customer=name.customer).update(mydate=mydate,payable_loan=(new_bal+amount),bal=int(amount+new_bal-amt_paid), balance=int(amount+new_bal-amt_paid)) 

                else:
                    CustomerLoan.objects.filter(customer=name.customer).update(payment ="Not owing any amount") 

        else:
            mydate =name.mydate - datetime.now()
            print(mydate,'days remaining')

            
    
   



