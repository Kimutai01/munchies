from django.shortcuts import render, HttpResponse
from vendor.models import Vendor



def home(request):
    clinics = Vendor.objects.filter(is_approved=True, user__is_active=True)[:5]
    print(clinics)
    
    context = {
        'clinics': clinics
    }
    
    return render(request, 'home.html', context)