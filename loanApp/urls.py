from django.urls import path
from .views import *
from .import views

app_name ="loanApp"



urlpatterns =[
    path('', views.home, name='home'),

    path('loan-request/', views.LoanRequest, name='loan_request'),
    path('loan_payment/', views.LoanPayment, name='loan_payment'),
    #path('user_transaction/', views.UserTrans, name='user_transaction'),
    path('user_transaction/', views.UserTransaction, name='user_transaction'),
    path('user_loan_history/', views.UserLoanHistory, name='user_loan_history'),

    path('user_dashboard/', views.UserDashboard, name='user_dashboard'),

    path('user-bank/', views.customerBank, name='user-bank'),
]



