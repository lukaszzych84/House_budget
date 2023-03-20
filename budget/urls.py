from budget import views
from django.urls import path
# from .views import expense_category_list
from django.urls import path
from .views import register, login_view
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('calculate/', views.calculate, name='calculate'),
    path('base/', views.base)
]