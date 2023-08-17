from django.shortcuts import render, HttpResponse, redirect
from .forms import UserForm
from django.contrib import messages
from vendor.forms import VendorForm
from .models import Profile
# Create your views here.

def registerUser(request):
    form = UserForm()
    
    if request.method == 'POST':
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
