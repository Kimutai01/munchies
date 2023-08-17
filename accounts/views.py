from django.shortcuts import render, HttpResponse, redirect
from .forms import UserForm
from django.contrib import messages
from vendor.forms import VendorForm
from .models import *
from django.contrib.auth.tokens import default_token_generator
from django.contrib import auth
from .utils import send_verification_email, detect_user
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from vendor.models import Vendor

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
            
            # send verification email
            send_verification_email(request,user)
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
            subject = 'Please activate your account'
            template = 'activate_account.html'
            send_verification_email(request,user,subject,template)
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
    redirect_url = detect_user(user)
    return redirect(redirect_url)
@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
    return render(request, 'customerDashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_clinic)
def clinicDashboard(request):
    clinic = Vendor.objects.get(user=request.user)
    context = {
        'clinic': clinic
    }
    return render(request, 'clinicDashboard.html', context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been verified successfully')
        return redirect('myAccount')
    else:
        messages.error(request, 'Activation link is invalid')
        return redirect('myAccount')
    
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
     
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            
            # send reset password email
            subject = 'Reset your password'
            template = 'reset_password_email.html'
            send_verification_email(request,user,subject,template)
            messages.success(request, 'Password reset email has been sent to your email address')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgot_password')
    return render(request, 'forgot_password.html')

def reset_password_validate(request, uidb64, token):
    # validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired')
        return redirect('myAccount')
    return

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('reset_password')
    return render(request, 'reset_password.html')
    
