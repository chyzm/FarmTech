from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User
from django.contrib import messages

# Create your views here

def registerUser(request):
    if request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']  # hashing password
            user = form.save(commit=False)            #this assigns a role to the user registring
            user.set_password(password)               # hashing password contd.
            user.role = User.CUSTOMER                 #this assigns a role to the user registring as a customer
            user.save()                               # this line saves the user
            messages.success(request, 'Account created successfully!')     # displays a success message when account is created before redirecting
            
            return redirect('registerUser')
        
        else:
            print('invalid form')
            print(form.errors)
    else:
      form = UserForm()
      
    context = {
        'form': form,
    }
        
    return render(request, 'accounts/registerUser.html', context)

