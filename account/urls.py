from django.urls import path
from .views import *
from .import views
#from loginApp import views


app_name = 'account'
urlpatterns = [
    path('login_customer/', views.login_view, name='login_customer'),
    path('signup-customer/', views.sign_up_view, name='signup_customer'),
    path('logout_customer/', views.logout_view, name='logout_customer'),
    path('edit-customer/', views.edit_customer, name='edit-customer'),
 
    path('customer-detail/',views.customerInfo, name='customer-detail'),
]
