
from django.urls import path, include
from . import views
from accounts import views as accounts_views

urlpatterns = [
    path('', accounts_views.clinicDashboard, name='clinic'),
    path('profile/', views.clinicProfile, name='clinic-profile'),
    path('opening-hours/', views.opening_hours, name='opening-hours'),
    path('bookings/', views.bookings, name='bookings'),
    
    path('opening-hours/add/', views.add_opening_hours, name='add-opening-hour'),
    # path('opening-hours/<int:pk>/delete/', views.delete_opening_hour, name='delete-opening-hour'),
    path('appointments/<int:pk>/', views.appointment_booking, name='appointments_booking'),
    path('edit-appointment/<int:pk>/', views.edit_appointment, name='edit-appointment'),
    path('delete-appointment/<int:pk>/', views.cancel_appointment, name='delete-appointment'),
    path('appointments/approve/<int:appointment_id>/', views.approve_appointment, name='approve_appointment'),
    path('appointments/reject/<int:appointment_id>/', views.reject_appointment, name='reject_appointment'),
    
]
