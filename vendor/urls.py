
from django.urls import path, include
from . import views
from accounts import views as accounts_views

urlpatterns = [
    path('', accounts_views.clinicDashboard, name='clinic'),
    path('profile/', views.clinicProfile, name='clinic-profile'),
]
