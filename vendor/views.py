from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import VendorForm
from accounts.forms import ProfileForm
from accounts.models import Profile
from django.shortcuts import get_object_or_404
from .models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from accounts.views import check_role_clinic, check_role_customer
from .forms import VendorForm, OpeningHourForm, AppointmentForm
from .models import OpeningHour, Appointment
from django.http import JsonResponse
from django.db import IntegrityError
from accounts.utils import send_notification

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

def opening_hours(request):
    opening_hours = OpeningHour.objects.filter(vendor=request.user.vendor)
    print(opening_hours)
    opening_hour_form = OpeningHourForm()
    
    context = {
        'opening_hours': opening_hours,
        'form': opening_hour_form
    }
    return render(request, 'opening_hours.html', context)

def add_opening_hours(request):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
            day = request.POST.get('day')
            from_hour = request.POST.get('from_hour')
            to_hour = request.POST.get('to_hour')
            is_closed = request.POST.get('is_closed')
            
            if is_closed == "True":  # Convert string to boolean
                is_closed = True
            else:
                is_closed = False

            try:
                hour = OpeningHour.objects.create(
                    vendor=request.user.vendor,
                    day=day,
                    from_hour=from_hour,
                    to_hour=to_hour,
                    is_closed=is_closed
                )
                
                hour.save()
                response = {'status': 'success'}
                return JsonResponse(response)
            except IntegrityError as e:
                response = {'status': 'failed'}
                return JsonResponse(response)

    return HttpResponse('add opening hours')

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def appointment_booking(request, pk):
    clinic = get_object_or_404(Vendor, pk=pk)
    user=request.user
    
    if user.appointment_set.filter(vendor=clinic).exists():
        messages.warning(request, 'You already have an appointment with this clinic. Please cancel your current appointment to book a new one.')
        return redirect('customerDashboard')
    
    else:
        form = AppointmentForm()
        if request.method == 'POST':
            form = AppointmentForm(request.POST)
            if form.is_valid():
                appointment = form.save(commit=False)
                appointment.user = user
                appointment.vendor = clinic
                appointment.save()
                messages.success(request, 'Your appointment has been booked!')
                return redirect('customerDashboard')
            else:
                print(form.errors)
        else:
            form = AppointmentForm()
            
    context = {
        'form': form,
        'clinic': clinic,
    }
    return render(request, 'appointment_booking.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def edit_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    form = AppointmentForm(instance=appointment)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your appointment has been updated!')
            return redirect('customerDashboard')
        else:
            print(form.errors)
    else:
        form = AppointmentForm(instance=appointment)
            
    context = {
        'form': form,
        'appointment': appointment,
    }
    return render(request, 'appointment_booking.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.delete()
    messages.success(request, 'Your appointment has been cancelled!')
    return redirect('customerDashboard')


def bookings(request):
    bookings = Appointment.objects.filter(vendor=request.user.vendor)
    print(bookings)
    context = {
        'bookings': bookings
    }
    return render(request, 'bookings.html', context)

def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.is_approved = True
    appointment.save()

    context = {'user': appointment.user}
    send_notification('Appointment Approved', 'approve_template.html', context)

    messages.success(request, 'Appointment approved successfully.')
    return redirect('bookings')

def reject_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.is_cancelled = True
    appointment.save()

    context = {'user': appointment.user}
    send_notification('Appointment Rejected', 'rejection_template.html', context)

    messages.success(request, 'Appointment rejected successfully.')
    return redirect('bookings')

