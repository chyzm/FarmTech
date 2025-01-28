from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.utils import detectUser
from vendor.forms import vendorform
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

# restrict farm from accessing customer page
def check_role_farm(user):
    if user.role == 1:
        return True
    
    else:
        raise PermissionDenied


# restrict customer from accessing farm page
def check_role_customer(user):
    if user.role == 2:
        return True
    
    else:
        raise PermissionDenied





def registerUser(request):
     # Checks if the user is already logged in
    if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in!')
            return redirect('dashboard')
        
    elif request.method == 'POST':
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
     # Checks if the user is already logged in
    if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in!')
            return redirect('dashboard')
        
    elif request.method  == 'POST':
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


# For login

from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

def login(request):
    # Checks if the user is already logged in
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')  # Redirect to the user's account page

    # Logs in the user if credentials are correct
    if request.method == 'POST':
        email = request.POST.get('email')  # Use .get() to avoid KeyError
        password = request.POST.get('password')  # Use .get() to avoid KeyError

        # Authenticate the user
        user = auth.authenticate(request, username=email, password=password)

        # If user credentials are correct
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in!')
            
            # Redirect based on user role
            if user.role == 1:  # Farmer
                return redirect('farmDashboard')   
            elif user.role == 2:   # Customer
                return redirect('customerDashboard')
            
        
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')  # Redirect back to the login page

    # Render the login page for GET requests
    return render(request, 'accounts/login.html')



# For logout

def logout(request):
    auth.logout(request)
    messages.info(request, 'logged out!')
    return redirect('login')



# My Account

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


# For dashboard
@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
     return render(request, 'accounts/customerDashboard.html')
 
 
 
@login_required(login_url='login')
@user_passes_test(check_role_farm)
def farmDashboard(request):
     return render(request, 'accounts/farmDashboard.html')