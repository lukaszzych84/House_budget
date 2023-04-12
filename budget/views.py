from pyexpat.errors import messages
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, UpdateView
from django.db.models import Sum
from .models import ExpenseCategory, IncomeCategory, Expense, Income
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages


#
# def expense_category_list(request):
#     expense_categories = ExpenseCategory.objects.all()
#     return render(request, 'main_page.html', {'expense_categories': expense_categories})

def home(request):
    if request.user.is_authenticated:
        # użytkownik jest zalogowany
        context = {'welcome_message': f'Witaj {request.user.username}!'}
    else:
        # użytkownik nie jest zalogowany
        context = {'welcome_message': 'Witaj na mojej stronie! Zarejestruj się lub zaloguj, aby korzystać z pełnej funkcjonalności.'}
    return render(request, 'budget/home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'budget/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
            return redirect('home')
        else:
            return HttpResponse(request, 'Nieprawidłowe dane.')

    else:
        form = AuthenticationForm()
        return render(request, 'budget/login.html', context={'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')  # przekierowanie na stronę logowania
@login_required(login_url='login')
def calculate(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        if amount and category_id and description:
            amount = float(amount)
            # category=  ExpenseCategory.objects.get(id=category_id)
            category = get_object_or_404(ExpenseCategory, id=category_id)
            Expense.objects.create(
                user=request.user,
                amount=amount,
                category=category,
                description=description
            )
            messages.success(request, "Dodano pomyślnie")
            return redirect('calculate')
    else:
        categories = ExpenseCategory.objects.all()
        return render(request, 'budget/calculate.html', context={'categories': categories})

@login_required(login_url='login')
def gift(request):
        if request.method == 'POST':
            amount = request.POST.get('amount')
            category_id = request.POST.get('category')
            description = request.POST.get('description')
            if amount and category_id and description:
                amount = float(amount)
                # category=  ExpenseCategory.objects.get(id=category_id)
                category = get_object_or_404(IncomeCategory, id=category_id)
                Income.objects.create(
                    user=request.user,
                    amount=amount,
                    category=category,
                    description=description
                )
                messages.success(request, "Dodano pomyślnie")
                return redirect('gift')
        else:
            categories = IncomeCategory.objects.all()
            return render(request, 'budget/gift.html', context={'categories': categories})

class ExpanseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'budget/expense_list.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sum_of_expenses'] = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        return context

class IncomeListView(LoginRequiredMixin, ListView):
    model = Income
    template_name = 'budget/income_list.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sum_of_incomes'] = Income.objects.aggregate(Sum('amount'))['amount__sum']
        return context



@login_required
def delete_income(request, income_id):
    income = Income.objects.get(id=income_id)
    income.delete()
    messages.success(request, f'Przychód został usunięty!')
    return redirect('income')
@login_required
def delete_expense(request, expense_id, ):
    expanse = Expense.objects.get(id=expense_id)
    expanse.delete()
    messages.success(request, f'Wydatek został usunięty!')
    return redirect('expense')

class IncomeUpdateView(LoginRequiredMixin, UpdateView):
    model = Income
    template_name = 'budget/income_edit.html'
    login_url = 'login'
    fields = ('description', 'amount')
    success_url = reverse_lazy('income')
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        return obj
    # def get_initial(self):
    #     initial = super().get_initial()
    #     initial['description'] = self.object.description
    #     initial['amount'] = self.object.amount
    #     return initial
class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    template_name = 'budget/expense_edit.html'
    login_url = 'login'
    fields = ('description', 'amount')
    success_url = reverse_lazy('expense')

# def base(request):
#     return render(request, template_name='base.html')

def about(request):
    return render(request, 'budget/about.html')