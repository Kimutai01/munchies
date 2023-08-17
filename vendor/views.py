from django.shortcuts import render

# Create your views here.

def clinicProfile(request):
    return render(request, 'clinic_profile.html')
