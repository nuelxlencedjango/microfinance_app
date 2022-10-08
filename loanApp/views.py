

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from account.models import *
from .forms import CustomerBankForm, LoanRequestForm, LoanTransactionForm, UpdateCustomerBankForm
from .models import *
from django.shortcuts import redirect
from account .forms import *
from django.contrib import messages
from django.http import HttpResponseRedirect

import datetime
from datetime import datetime, timedelta
from django.urls import reverse
from django.db.models import Sum
# Create your views here.



def home(request):
    present = datetime.now()+timedelta(days=30)
    today = datetime.now()

    if request.user.is_authenticated:
        abb = CustomerLoan.objects.filter(customer=request.user)
        tr =loanTransaction.objects.filter(customer=request.user)

        return render(request, 'new/general/index.html', context={'abb':abb})
      
    return render(request, 'new/general/index.html', context={'present':present,'today':today})
   



@login_required(login_url='/account/login-customer')
def LoanRequest(request):

    if CustomerLoan.objects.filter(customer=request.user).exists():
        if loanTransaction.objects.filter(customer = request.user).exists():
            
            totalPayable = CustomerLoan.objects.filter(customer=request.user).aggregate(
            Sum('payable_loan'))['payable_loan__sum']
            totalPaid = loanTransaction.objects.filter(customer=request.user).aggregate(Sum('payment'))[
            'payment__sum']

            if totalPayable > totalPaid:
                messages.warning(request, 'Please pay up your outstanding balance before you can request for another loan')
                return redirect('loanApp:user_dashboard') 
            
            form = LoanRequestForm()
            if request.method == 'POST':
                form = LoanRequestForm(request.POST)
                if form.is_valid():
                    loan_obj = form.save(commit=False)
                    loan_obj.customer = request.user
                    loan_obj.save()

                    messages.warning(request, 'Request recieved.We will get back to you soon')
                    return redirect('/')
            
            return render(request, 'loanapp/loanrequest.html', context={'form': form})  

        messages.warning(request, 'Please start making payment so you can request for another')
        return redirect('loanApp:user_dashboard') 
            
    
    elif CustomerInfo.objects.filter(user=request.user).exists() and CustomerBank.objects.filter(user=request.user):

        form = LoanRequestForm()
        
        if request.method == 'POST':
            form = LoanRequestForm(request.POST)
            if form.is_valid():
                loan_obj = form.save(commit=False)
                loan_obj.customer = request.user
                loan_obj.save()

                messages.warning(request, 'Request recieved.We will get back to you soon')
                return redirect('/')

        return render(request, 'loanapp/loanrequest.html', context={'form': form})


    elif  CustomerInfo.objects.filter(user=request.user).exists():
       
        form =CustomerBankForm()
        context={'form': form}
        return render(request, 'loanapp/customerBank.html', context)

    else:
       
        form=CustomerInfoForm()  
        context={'form': form}
        return render(request, 'loginApp/customerDetail.html', context)



@login_required(login_url='/account/login-customer')
def LoanPayment(request):
    form = LoanTransactionForm()
    if request.method == 'POST':
        form = LoanTransactionForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.customer = request.user
            payment.save() 

            totalPayable = CustomerLoan.objects.filter(customer=request.user).aggregate(
                Sum('payable_loan'))['payable_loan__sum']

            totalPaid = loanTransaction.objects.filter(customer=request.user).aggregate(Sum('payment'))[
            'payment__sum']
            CustomerLoan.objects.filter(customer=request.user).update(total_amount_paid=totalPaid, balance=int(totalPayable-totalPaid),bal=int(totalPayable-totalPaid))

            if totalPayable == totalPaid:
                CustomerLoan.objects.filter(customer=request.user).update(payment="Fully paid")
                
            messages.warning(request,'payment acknowledged ')
            return redirect('/')

        messages.warning(request,'Payment not successful')
    return render(request, 'loanApp/payment.html', context={'form': form})




@login_required(login_url='/account/login-customer')
def UserTransaction(request):
    if loanTransaction.objects.filter(customer=request.user).exists():

        transactions = loanTransaction.objects.filter(customer=request.user)
        return render(request, 'loanapp/user_transaction.html', context={'transactions': transactions})#,"bal":bal})

    messages.warning(request,'You dont have any transaction yet')
    return render(request, 'loanapp/user_transaction.html')



@login_required(login_url='/account/login-customer')
def UserLoanHistory(request):
    loans = loanRequest.objects.filter(customer=request.user)
    get_info = CustomerLoan.objects.filter(customer=request.user)

    context={'loans': loans,'get_info':get_info}
    
    return render(request, 'loanApp/user_loan_history.html', context)





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



def error_404_view(request, exception):
    print("not found")
    return render(request, 'notFound.html')




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




def aboutUs(request):
    return render(request, 'new/general/about.html')



def ourServices(request):
    return render(request, 'new/general/services.html')



def contactUs(request):
    return render(request, 'new/general/contact.html')

      


