from django.shortcuts import render, redirect
from django.http import HttpResponse
from vendor.forms import vendorform
from .forms import UserForm
from .models import User, UserProfile
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


# For vendor resgistration

def registerVendor(request):
    if request.method  == 'POST':
        # store the data and create the user 
        form = UserForm(request.POST)
        v_form = vendorform(request.POST, request.FILES) # request.FILES because vendors will be uploading a file
        
        
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.FARM                        #this assigns a role to the user registring as a FArm
            user.save()                                       # this line saves the user
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            
            
            messages.success(request, 'Account created successfully! Please wait for approval')     # displays a success message when account is created before redirecting
            
            return redirect('registerVendor')
        
        else: 
              messages.error(request, 'Form submission failed. Please check the details and try again.')
              print('Invalid form submission')
              print(form.errors)
              print(v_form.errors)
             
        
    
    
    # We want the vendor form to use fields from user registration form. Also makes the fields editable on the form
    else:
        form = UserForm()
        v_form = vendorform()
    
    context = {
        'form' : form,
        'v_form' : v_form,
        
    }
    
    # Render
    
    return render(request, 'accounts/registerVendor.html', context)

