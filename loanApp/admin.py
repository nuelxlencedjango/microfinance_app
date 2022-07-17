from django.contrib import admin
from .models import *
# Register your models here.loanCategory,
admin.site.register(CustomerBank)
admin.site.register(loanCategory)
admin.site.register(loanRequest)
admin.site.register(CustomerLoan)
admin.site.register(loanTransaction)
admin.site.register(Repayment)

