from django.contrib import admin
from .models import ExpenseCategory, IncomeCategory, Income, Expense

admin.site.register(ExpenseCategory)
admin.site.register(IncomeCategory)
admin.site.register(Income)
admin.site.register(Expense)


