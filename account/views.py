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

    form = UserUpdateForm(instance=request.user)
    form2 = CustomerInfoForm(instance=request.user.customer_info)
    
    if request.method == 'POST':

        form = UserUpdateForm(request.POST,  instance = request.user)
        form2 = CustomerInfoForm(request.POST,request.FILES,instance=request.user.customer_info)
   
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
        
            return HttpResponseRedirect(reverse('loanApp:home'))
 
        context={'form': form,'form2':form2}
        return render(request, 'loginApp/update/edit.html', context)


    context={'form': form,'form2':form2}
    return render(request, 'loginApp/update/edit.html',context)       




@login_required(login_url='/account/login-customer')
def edit_password(request):

    form = UserUpdatePasswordForm(instance=request.user)
    if request.method == 'POST':

        form = UserUpdatePasswordForm(request.POST,  instance = request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('loanApp:home'))
 
        context={'form': form}
        return render(request, 'loginApp/update/edit_password.html', context)


    context={'form': form}
    return render(request, 'loginApp/update/edit_password.html',context) 




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




def editCustomer(request):

    return render(request, 'loginApp/update/edit_info.html') 


