
from pyexpat.errors import messages

from django.contrib.auth import authenticate, login, logout

from .forms import AdminLoginForm

from django.shortcuts import render ,redirect ,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test

from loanApp.models import loanCategory, loanRequest, CustomerLoan, loanTransaction
from .forms import LoanCategoryForm

from account.models import *
from django.contrib.auth.models import User
from django.db.models import Q 
from datetime import date
from django.contrib import messages
from django.db.models import Sum

from django.views.generic import (
    ListView 
)
from datetime import datetime, timedelta
# Create your views here.



#superuser login
def superuser_login_view(request):

    form = AdminLoginForm()
    #if alredy logged in,go to home page
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    #if not logged in yet    
    else:
        if request.method == 'POST':
            #admin login form
            form = AdminLoginForm(data=request.POST)
            #check data given
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                
                #athenticate the user
                user = authenticate(request, username=username, password=password)
                
                #if user exists
                if user is not None:
                    # check if user is a superuser
                    if user.is_superuser:
                        login(request, user)
                       
                        return HttpResponseRedirect(reverse('adminManager:dashboard'))
                    #show this page    
                    else:
                        return render(request, 'admin/adminLogin.html', context={'form': form, 'error': "You are not Super User"})

            else:

                return render(request, 'admin/adminLogin.html', context={'form': form, 'error': "Invalid Username or Password "})
    return render(request, 'admin/adminLogin.html', context={'form': form, 'user': "Admin Login"})




# @user_passes_test(lambda u: u.is_superuser)
@staff_member_required(login_url='/manager/admin-login')
def dashboard(request):

    #get number of total users,requested loan,approved loans,rejected loans.total loan given,total reurned amoun
    # toal amount paid 
    totalCustomer = CustomerInfo.objects.all().count(),
    requestLoan = loanRequest.objects.all().filter(status='pending').count(),
    approved = loanRequest.objects.all().filter(status='approved').count(),
    rejected = loanRequest.objects.all().filter(status='rejected').count(),

    totalLoan = CustomerLoan.objects.aggregate(Sum('total_loan'))['total_loan__sum'],
    totalPayable = CustomerLoan.objects.aggregate(Sum('payable_loan'))['payable_loan__sum'],
    totalPaid = loanTransaction.objects.aggregate(Sum('payment'))['payment__sum'],

    dict = {
        'totalCustomer': totalCustomer[0],
        'request': requestLoan[0],
        'approved': approved[0],
        'rejected': rejected[0],
        'totalLoan': totalLoan[0],
        'totalPayable': totalPayable[0],
        'totalPaid': totalPaid[0],

    }
  
    
    # get list of all customers
    all_customer =CustomerLoan.objects.all()
    #iterating through the list
    for name in all_customer:
        #check expected date of payment
        if int(datetime.now().strftime("%s")) == int(name.mydate.strftime("%s")):
            amount_payable = CustomerLoan.objects.filter(customer=name.customer)
           
            for amt in amount_payable:
                amount = amt.payable_loan
                amt_paid = amt.total_amount_paid
                
                # if there's outstanding
                if int(amount) > int(amt_paid):
                    new_bal =amount - amt_paid

                   # add 10% to outstanding
                    new_bal = (new_bal *10) / 100
                    mydate = datetime.now() + timedelta(days=1)
                    
                    #update account
                    CustomerLoan.objects.filter(customer=name.customer).update(mydate=name.mydate,
                    payable_loan=(new_bal+amount),bal=int(amount+new_bal-amt_paid),
                     balance=int(amount+new_bal-amt_paid)) 
                
                #update account to 'Not owing any amount' if not owing any amount
                else:
                    CustomerLoan.objects.filter(customer=name.customer).update(payment ="Not owing any amount") 

        else:

            mydate =int(name.mydate.strftime("%s")) - int(datetime.now().strftime("%s"))
            
    return render(request, 'admin/dashboard.html', context=dict)



#adding more categories
@staff_member_required(login_url='/manager/admin-login')
def add_category(request):
    form = LoanCategoryForm()
    if request.method == 'POST':
        #input from the user
        form = LoanCategoryForm(request.POST)
        #check data given and save
        if form.is_valid():
            form.save()
            return redirect('managerApp:dashboard')
    return render(request, 'admin/admin_add_category.html', {'form': form})


#all users and customer details
@staff_member_required(login_url='/manager/admin-login')
def total_users(request):
    users = User.objects.all()
    users_detail = CustomerInfo.objects.all()

    context={'users': users,'users_details':users_detail}
    return render(request, 'admin/customer.html', context)


# login before removing users from the list
@staff_member_required(login_url='/manager/admin-login')
def user_remove(request, pk):
    #get the id of the customer to delete
    CustomerInfo.objects.get(id=pk).delete()
    user = User.objects.get(id=pk)
    #remove
    user.delete()
    return HttpResponseRedirect('/manager/users')
    

#login to get the list of loan requests
@staff_member_required(login_url='/manager/admin-login')
def loan_request(request):
    loanrequest = loanRequest.objects.filter(status='pending')
    return render(request, 'admin/request_user.html', context={'loanrequest': loanrequest})


#login to see a customer's transactions
@staff_member_required(login_url='/manager/admin-login')
def approved_request(request, id):
    today = date.today()
    status_date = today.strftime("%B %d, %Y")
    loan_obj = loanRequest.objects.get(id=id)
    loan_obj.status_date = status_date
    loan_obj.save()
  
    approved_customer = loanRequest.objects.get(id=id).customer
    if CustomerLoan.objects.filter(customer=approved_customer).exists():

        # find previous amount of customer
        PreviousAmount = CustomerLoan.objects.get(customer=approved_customer).total_loan
        PreviousPayable = CustomerLoan.objects.get(customer=approved_customer).payable_loan

        # update balance
        CustomerLoan.objects.filter(customer=approved_customer).update(total_loan=int(PreviousAmount)+int(loan_obj.amount))
        CustomerLoan.objects.filter( customer=approved_customer).update(payable_loan=int(PreviousPayable)+int(loan_obj.amount)+int(loan_obj.amount)*0.10)# *int(year))
       
    

    else:
        # CustomerLoan object create
        save_loan = CustomerLoan()

        save_loan.customer = approved_customer
        save_loan.total_loan = int(loan_obj.amount)
        save_loan.payable_loan = int(loan_obj.amount)+int(loan_obj.amount)*0.10 #*int(year)
        save_loan.save()
       
       
    loanRequest.objects.filter(id=id).update(status='approved')
    loanrequest = loanRequest.objects.filter(status='pending')

    save_loan = CustomerLoan()
    save_loan.payable_loan = int(loan_obj.amount)+int(loan_obj.amount)*0.10 #*int(year) 

    loanRequest.objects.filter(id=id, customer=approved_customer).update(total_payment= save_loan.payable_loan)  
    return render(request, 'admin/request_user.html', context={'loanrequest': loanrequest})



#login to loans rejected and the dates
@staff_member_required(login_url='/manager/admin-login')
def rejected_request(request, id):

    today = date.today()
    status_date = today.strftime("%B %d, %Y")
    loan_obj = loanRequest.objects.get(id=id)

    #assign today as the date of transactions 
    loan_obj.status_date = status_date
    loan_obj.save()
    # update if rejected
    loanRequest.objects.filter(id=id).update(status='rejected')
    loanrequest = loanRequest.objects.filter(status='pending')
    return render(request, 'admin/request_user.html', context={'loanrequest': loanrequest})


#login to  approve loans
@staff_member_required(login_url='/manager/admin-login')
def approved_loan(request):
    approvedLoan = loanRequest.objects.filter(status='approved')
  
    return render(request, 'admin/approved_loan.html', context={'approvedLoan': approvedLoan})#,'profit':profit})


#login to reject loan request
@staff_member_required(login_url='/manager/admin-login')
def rejected_loan(request):
    rejectedLoan = loanRequest.objects.filter(status='rejected')
    return render(request, 'admin/rejected_loan.html', context={'rejectedLoan': rejectedLoan})


#list of loan transaction
@staff_member_required(login_url='/manager/admin-login')
def transaction_loan(request):
    transactions = loanTransaction.objects.all()
    return render(request, 'admin/transaction.html', context={'transactions': transactions})



#login to get customer all details
@staff_member_required(login_url='/manager/admin-login')
def detailedCustomerInfo(request,pk):
    user =get_object_or_404(User,id=pk)
    
    # check loanreques,customerloan and loan transaction if a customer exists
    if loanRequest.objects.filter(customer=user).exists() and CustomerLoan.objects.filter(customer=user) and loanTransaction.objects.filter(customer=user).exists():
       
       #All detailed information of a customer
        loan_info = loanRequest.objects.filter(customer=user,status='approved')
        customer_info = CustomerLoan.objects.filter(customer=user)
        loan_transact = loanTransaction.objects.filter(customer=user)
      
        total_loaned_amount = loanRequest.objects.filter(customer=user).aggregate(
            Sum('amount'))['amount__sum']

        total_return_amount = loanRequest.objects.filter(customer=user).aggregate(
            Sum('total_payment'))['total_payment__sum']

        total_profit = loanRequest.objects.filter(customer=user).aggregate(
            Sum('profit'))['profit__sum']  

        total_payment_made = loanTransaction.objects.filter(customer=user).aggregate(
            Sum('payment'))['payment__sum'] 
              
        CustomerLoan.objects.filter(customer=user).update(bal=total_payment_made)       
        
        all="doing good"

        context={'loan_info':loan_info,'customer_info':customer_info,'loan_transact':loan_transact,
        'all':all,'user':user,'total_loaned_amount':total_loaned_amount,'total_return_amount':total_return_amount,
        'total_profit':total_profit,'total_payment_made':total_payment_made}

        return render(request, 'admin/customer_loan_detail.html', context)

    # if customer exists in loan request, customerloan , must not owe anything before making any request
    elif loanRequest.objects.filter(customer=user).exists() and CustomerLoan.objects.filter(customer=user):
        loan_info = loanRequest.objects.filter(customer=user,status='approved')
        customer_info = CustomerLoan.objects.filter(customer=user)

        messages.warning(request,'This customer has not made any payment')
        yet_to_pay ="not paid"
        context={'loan_info':loan_info,'customer_info':customer_info,'yet_to_pay':yet_to_pay,'user':user}
        
        return render(request, 'admin/customer_loan_detail.html', context)

    else:
        loan_info = loanRequest.objects.filter(customer=user,status='approved')
        pend =""
        context={'loan_info':loan_info,'pend':pend,'user':user}

        return render(request, 'admin/customer_loan_detail.html', context)

        

def getLocation(request): 
    return render(request,'admin/location.html')


#search for location,total amount given in that location
@staff_member_required(login_url='/manager/admin-login')
def searchLocation(request):
    query = request.GET.get('search')
    location = Location.objects.filter(Q(area__icontains =query))
    if location and CustomerInfo.objects.filter(location__in=location):

        names = CustomerInfo.objects.filter(location__in=location)

        persons =[]
        amt=[]
        exp =[]

        total_payment=[]
        balance=[]
        amt_paid=[]
        #profit =[]

        for name in names:
            pp =CustomerLoan.objects.filter(customer=name.user)
            loan = loanRequest.objects.filter(customer=name.user)
            for n in pp:
            #a =pp.total_loan
                persons.append(n.customer)
                amt.append(n.total_loan)
                exp.append(n.payable_loan)
                balance.append(n.balance)
                total_payment.append(n.total_amount_paid)

            for name in loan:
                amt_paid.append(name.total_payment)

                
        total_amount_loan =sum(amt)
        totalPay =sum(total_payment)
        totalExpected = sum(exp)
        totalBalance = sum(balance)

        context ={'persons':persons,'amt':amt,'exp':exp,'balance':balance,
        'total_payment':total_payment,'location':location,
        'total_amount_loan':total_amount_loan,'totalPay':totalPay,'totalExpected':totalExpected,#'profit':profit,
   
        'totalExpected':totalExpected,'totalBalance':totalBalance}

        return render(request, 'admin/location_detail.html', context)

    return render(request, 'admin/location_detail.html')    
        
        


class SearchResultsView(ListView):
    model = Location
    template_name = 'admin/location_detail.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('search')
        product=Location.objects.get(Q(area__icontains=query))
        persons = CustomerInfo.objects.filter(location=product)
        for per in persons:
            pp =CustomerLoan.objects.filter(customer=per.user)
            for d in pp:
                n =CustomerLoan.objects.filter(customer=d.customer)
                if loanRequest.objects.filter(customer=d.customer):
                    v =loanRequest.objects.filter(customer=d.customer)
                    #print(v[0])
 

        return v


      