from django.shortcuts import render, HttpResponse, redirect
from .forms import UserForm
from django.contrib import messages
from vendor.forms import VendorForm
from .models import Profile
from django.contrib import auth
from .utils import detectUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
# Create your views here.

def check_role_clinic(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
    
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('dashboard')
    
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.role = user.CUSTOMER
            user.set_password(password)
            user.save()
            messages.success(request, 'Your account has been created successfully')
            return redirect('register-user')
        else:
            print('Form is not valid')
            print(form.errors)
    else:
        form = UserForm()
    
    context = {
        'form': form
    }
    return render(request, 'registerUser.html', context)

def registerVendor(request):
    form = UserForm()
    vendorForm = VendorForm()
    
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        vendorForm = VendorForm(request.POST, request.FILES)
        if form.is_valid() and vendorForm.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.role = user.CLINIC
            user.set_password(password)
            user.save()
            vendor = vendorForm.save(commit=False)
            vendor.user = user
            profile = Profile.objects.get(user=user)
            vendor.profile = profile
            vendor.save()
            messages.success(request, 'Your account has been created successfully, please wait for the approval')
            return redirect('register-vendor')
        else:
            print('Form is not valid')
            print(form.errors)
            print(vendorForm.errors)
    else:
        form = UserForm()
        vendorForm = VendorForm()
    context = {
        'form': form,
        'vendorForm': vendorForm,
        
    }
    return render(request, 'registerVendor.html', context)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('myAccount')
    
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'You are now logged out')
    return redirect('login')


@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirect_url = detectUser(user)
    return redirect(redirect_url)
@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
    return render(request, 'customerDashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_clinic)
def clinicDashboard(request):
    return render(request, 'clinicDashboard.html')
