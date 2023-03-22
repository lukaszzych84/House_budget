from pyexpat.errors import messages
from django.utils import timezone
from .models import ExpenseCategory, IncomeCategory, Expense
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
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'budget/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # obsługa błędnego logowania
            pass
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

def base(request):
    return render(request, template_name='base.html')