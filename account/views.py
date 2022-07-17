from multiprocessing import context
from unicodedata import name
from urllib import request
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

from loanApp.forms import CustomerBankForm
from .forms import *
from django.shortcuts import redirect
from .models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.


def sign_up_view(request):
    error = ''
    if request.user.is_authenticated:

        return HttpResponseRedirect(reverse('loanApp:home'))

    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        #form2 = CustomerDetailsForm(request.FILES, request.POST)
       # print(form.cleaned_data['username'])
        if form.is_valid(): #and form2.is_valid():
            user = form.save()
            user.save()         
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
      
            user = authenticate(request, username=username, password=password1)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('loanApp:home'))

            return HttpResponseRedirect(reverse('account:login_customer'))

        else:
            if User.objects.filter(username=request.POST['username']).exists():
                error = 'A customer with this username already exists'

            else:
                error = 'Your password is not strong enough or both password must be same'
        

    return render(request, 'loginApp/signup.html', context={'form': form,  'user': "Customer Register", 'error': error})


         

 














def login_view(request):
    form = CustomerLoginForm()
    if request.method == 'POST':
        form = CustomerLoginForm(data=request.POST)
      
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('loanApp:home'))

        else:
            return render(request, 'loginApp/login.html', context={'form': form, 'user': "Customer Login", 'error': 'Invalid username or password'})
    return render(request, 'loginApp/login.html', context={'form': form, 'user': "Customer Login"})






@login_required()
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('loanApp:home'))





@login_required(login_url='/account/login-customer')
def edit_customer(request):
    #user = User.objects.get(user=request.user)
    customer = CustomerInfo.objects.get(user=request.user)
    form = UpdateCustomerForm(instance=customer)
    if request.method == 'POST':

        form = UpdateCustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid:
            customer = form.save(commit=False)
            customer.save()
            return HttpResponseRedirect(reverse('home'))
    # return HttpResponseRedirect(reverse('home'))
    
    return render(request, 'loginApp/edit.html', context={'form': form})


 




def customerInfo(request):
    form = CustomerInfoForm()
    
    if request.method == "POST":
        form = CustomerInfoForm(request.POST,request.FILES)

        if form.is_valid():
            user = request.user
            info = form.save(commit=False)
            info.user = user
            info.save()

            form =CustomerBankForm()
            context ={'form':form}

            return render(request,'loanapp/customerBank.html',context)
    

        form=CustomerInfoForm()  
        context={'form':form}
        return render(request, 'loginApp/customerDetail.html', context)
       

    return redirect('loanApp:home')  





