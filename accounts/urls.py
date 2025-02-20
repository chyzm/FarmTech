from django.urls import path
from . import views

urlpatterns = [
     path('registerUser/', views.registerUser, name='registerUser'),
     path('registerVendor/', views.registerVendor, name='registerVendor'),
     path('login/', views.login, name='login'),
     path('logout/', views.logout, name='logout'),
     path('myAccount/', views.myAccount, name='myAccount'),
     path('customerDashboard/', views.customerDashboard, name='customerDashboard'),
     path('farmDashboard/', views.farmDashboard, name='farmDashboard'),
]
