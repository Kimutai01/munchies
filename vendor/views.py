from django.shortcuts import render, redirect
from .forms import VendorForm
from accounts.forms import ProfileForm
from accounts.models import Profile
from django.shortcuts import get_object_or_404
from .models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from accounts.views import check_role_clinic

# Create your views here.



    
    
@login_required(login_url='login')
@user_passes_test(check_role_clinic)
def clinicProfile(request):
    profile = get_object_or_404(Profile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    profile_form = ProfileForm(instance=profile)
    vendor_form = VendorForm(instance=vendor)
    
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Your profile has been updated!')
            redirect('clinic-profile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
           
    else:
        profile_form = ProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
    
    
    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'clinic_profile.html', context)
