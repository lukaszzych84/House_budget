from django.urls import path
from .views import register, login_view
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('calculate/', views.calculate, name='calculate'),
    path('gift/', views.gift, name='gift'),
    path('expense/', views.ExpanseListView.as_view(), name='expense'),
    path('income/', views.IncomeListView.as_view(), name='income'),
    path('income/<int:income_id>/delete/', views.delete_income, name='income_delete'),
    path('expense/<int:expense_id>/delete/', views.delete_expense, name='expense_delete'),
    path('expense/<int:pk>/update/', views.ExpenseUpdateView.as_view(), name='expense_edit'),
    path('income/<int:pk>/update/', views.IncomeUpdateView.as_view(), name='income_edit')




    # path('base/', views.base)
]