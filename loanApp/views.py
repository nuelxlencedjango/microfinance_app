

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from account.models import *
from .forms import CustomerBankForm, LoanRequestForm, LoanTransactionForm, UpdateCustomerBankForm
from .models import *
from django.shortcuts import redirect
from account .forms import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import datetime
from datetime import datetime, timedelta
from django.urls import reverse
from django.db.models import Sum
# Create your views here.



def home(request):
    #getting today's date
    present = datetime.now()+timedelta(days=30)
    today = datetime.now()
    
    #checking if user is logged in
    if request.user.is_authenticated:
        abb = CustomerLoan.objects.filter(customer=request.user)
        tr =loanTransaction.objects.filter(customer=request.user)

        return render(request, 'new/general/index.html', context={'abb':abb})
      
    return render(request, 'new/general/index.html', context={'present':present,'today':today})
   


#login function
@login_required(login_url='/account/login-customer')
def LoanRequest(request):
    
    #check user existence and get user's details
    if CustomerLoan.objects.filter(customer=request.user).exists():
        if loanTransaction.objects.filter(customer = request.user).exists():
            
            totalPayable = CustomerLoan.objects.filter(customer=request.user).aggregate(
            Sum('payable_loan'))['payable_loan__sum']
            totalPaid = loanTransaction.objects.filter(customer=request.user).aggregate(Sum('payment'))[
            'payment__sum']
            #if user is owing,direct to user's dashboard
            if totalPayable > totalPaid:
                messages.warning(request, 'Please pay up your outstanding balance before you can request for another loan')
                return redirect('loanApp:user_dashboard') 
            
            #loan request form if user doesnt owe
            form = LoanRequestForm()
            if request.method == 'POST':
                form = LoanRequestForm(request.POST)
                #if data given is valid,save and direct to home page
                if form.is_valid():
                    loan_obj = form.save(commit=False)
                    loan_obj.customer = request.user
                    loan_obj.save()

                    messages.warning(request, 'Request recieved.We will get back to you soon')
                    return redirect('/')
            
            return render(request, 'loanapp/loanrequest.html', context={'form': form})  

        messages.warning(request, 'Please start making payment so you can request for another')
        return redirect('loanApp:user_dashboard') 
            
    #if user details are not complete, give form to complete user's form
    elif CustomerInfo.objects.filter(user=request.user).exists() and CustomerBank.objects.filter(user=request.user):

        form = LoanRequestForm()
        
        if request.method == 'POST':
            #if loan reques form is valid,save and redirect to home page
            form = LoanRequestForm(request.POST)
            if form.is_valid():
                loan_obj = form.save(commit=False)
                loan_obj.customer = request.user
                loan_obj.save()

                messages.warning(request, 'Request recieved.We will get back to you soon')
                return redirect('/')

        return render(request, 'loanapp/loanrequest.html', context={'form': form})

    #user's details form
    elif  CustomerInfo.objects.filter(user=request.user).exists():
       
        form =CustomerBankForm()
        context={'form': form}
        return render(request, 'loanapp/customerBank.html', context)

    else:
       
        form=CustomerInfoForm()  
        context={'form': form}
        return render(request, 'loginApp/customerDetail.html', context)



#login before a user can make payment
@login_required(login_url='/account/login-customer')
def LoanPayment(request):
    form = LoanTransactionForm()
    if request.method == 'POST':
        form = LoanTransactionForm(request.POST)
        #check vaidity of the data given,save if correct
        if form.is_valid():
            payment = form.save(commit=False)
            payment.customer = request.user
            payment.save() 
            
            #user's loan request and payment
            totalPayable = CustomerLoan.objects.filter(customer=request.user).aggregate(
                Sum('payable_loan'))['payable_loan__sum']

            totalPaid = loanTransaction.objects.filter(customer=request.user).aggregate(Sum('payment'))[
            'payment__sum']
            CustomerLoan.objects.filter(customer=request.user).update(total_amount_paid=totalPaid, balance=int(totalPayable-totalPaid),bal=int(totalPayable-totalPaid))
            
            #if total amount paid is same as the expected reurns
            if totalPayable == totalPaid:
                CustomerLoan.objects.filter(customer=request.user).update(payment="Fully paid")
                
            messages.warning(request,'payment acknowledged ')
            return redirect('/')
         #else send message warning
        messages.warning(request,'Payment not successful')
    return render(request, 'loanApp/payment.html', context={'form': form})




#user should login  to see all transactions
@login_required(login_url='/account/login-customer')
def UserTransaction(request):
    if loanTransaction.objects.filter(customer=request.user).exists():

        transactions = loanTransaction.objects.filter(customer=request.user)
        return render(request, 'loanapp/user_transaction.html', context={'transactions': transactions})#,"bal":bal})

    messages.warning(request,'You dont have any transaction yet')
    return render(request, 'loanapp/user_transaction.html')



#user should login  to see all loan requuest and approved loan
@login_required(login_url='/account/login-customer')
def UserLoanHistory(request):
    #if loanRequest.objects.filter(customer=request.user).exists():
    try:
        loans = loanRequest.objects.filter(customer=request.user)
        get_info = CustomerLoan.objects.filter(customer=request.user)

        context={'loans': loans,'get_info':get_info}
    
        return render(request, 'loanApp/user_loan_history.html', context)

    except Exception as e:

        messages.success(request, 'You dont have any loan histry yet.')
        return render(request, 'loanApp/user_loan_history.html')

    #loans = loanRequest.objects.filter(customer=request.user)
    #get_info = CustomerLoan.objects.filter(customer=request.user)

   




#user's dashboard.user has to log in to see 
@login_required(login_url='/account/login-customer')
def UserDashboard(request):
    requestLoan = loanRequest.objects.filter(customer=request.user).count()
    approved = loanRequest.objects.filter(customer=request.user,status='approved').count()
    rejected = loanRequest.objects.filter(customer=request.user,status='rejected').count()
    
    totalLoan = CustomerLoan.objects.filter(customer=request.user).aggregate(Sum('total_loan'))[
      'total_loan__sum']

    totalPayable = CustomerLoan.objects.filter(customer=request.user).aggregate(
        Sum('payable_loan'))['payable_loan__sum']
        
    totalPaid = loanTransaction.objects.filter(customer=request.user).aggregate(Sum('payment'))[
        'payment__sum']

     
    dict = {
        'request': requestLoan,
        'approved': approved,
        'rejected': rejected,
        'totalLoan': totalLoan,
        'totalPayable': totalPayable,
        'totalPaid': totalPaid,
        #'newLoan': newLoan
    }

    return render(request, 'loanapp/user_dashboard.html', context=dict)


#not found page
def error_404_view(request, exception):
    print("not found")
    return render(request, 'notFound.html')



#user's bank details
def customerBank(request):
    form = CustomerBankForm()
    if request.method == "POST":
        form = CustomerBankForm(request.POST)

        if form.is_valid():
            user = request.user
            info = form.save(commit=False)
            info.user = user
            info.save()

            return redirect('loanApp:loan_request')  

        form=CustomerBankForm()  
        err ="errors"
        context ={'form':form, "err":err}
        return render(request, 'loanapp/customerBank.html', context)
       

    return redirect('loanApp:home')  



#user to edit bank information
@login_required(login_url='/account/login-customer')
def edit_bank(request):
    form = UpdateCustomerBankForm(instance=request.user.customer_bank)
    if request.method == 'POST':

        form =UpdateCustomerBankForm(request.POST,  instance = request.user.customer_bank)
        if form.is_valid():
            form.save()
            messages.warning(request,'Successfully updated')
            return HttpResponseRedirect(reverse('loanApp:home'))
 
        context={'form': form}
        messages.warning(request,'Form is not valid')
        return render(request, 'loginApp/update/edit_bank.html', context)


    context={'form': form}
    return render(request, 'loginApp/update/edit_bank.html',context) 



#about page
def aboutUs(request):
    return render(request, 'new/general/about.html')


#types of service page
def ourServices(request):
    return render(request, 'new/general/services.html')


#contact page
def contactUs(request):
    return render(request, 'new/general/contact.html')

      


