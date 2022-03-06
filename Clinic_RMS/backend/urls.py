"""Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    # URL path of the Home page of system
    # Uses by admin only and this check ed by 'admin_only' decorator
    path("", views.adminDashboard, name="admin_dashboard"),

    # URL path of register page
    path('register/', views.register, name="register"),

    # URL path of Login page
    path('login/', views.loginUser, name="login"),

    # URL path of client dashboerd
    path("client/<str:name>", views.clientDashboard, name="client_dashboard"),

    # URL path of logout and back again to the home page
    path('logout/', views.logoutUser, name='logout'),
    
    # URL path of reset password page
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(template_name='backend/password_reset.html'),
        name="password_reset"
        ),

    # URL path of the confirmed operation of sending mail to the client to reset his password again
    path(
        "reset_password_sent/", 
        auth_views.PasswordResetDoneView.as_view(template_name='backend/password_reset_sent.html'), 
        name="password_reset_done"
        ),

    # URL path of the form that used to reset new password
    path(
        "reset/<uidb64>/<token>", 
        auth_views.PasswordResetConfirmView.as_view(template_name='backend/password_reset_form.html'), 
        name="password_reset_confirm"
        ),

    # URL path of the page that confirmed that your password is being changed
    path(
        "reset_password_complete/", 
        auth_views.PasswordResetCompleteView.as_view(template_name='backend/password_reset_done.html'), 
        name="password_reset_complete"
        ),

    # URL path of page that views all the appointments
    path('all_appointments/', views.allAppointments, name='all_appointments'),

    # URL path of page that views the past appointments
    path('past_appointments/', views.pastAppointments, name='past_appointments'),

    # URL path of page that views the upcoming appointments
    path('upcoming_appointments/', views.upcomingAppointments, name='upcoming_appointments'),

    # URL path of page that views the resheduled appointments
    path('rescheduled_appointments/', views.rescheduledAppointments, name='rescheduled_appointments'),

    # URL path of the form that's used to reserve a new appointment
    path('client_reserve_appointment/', views.clientReserveAppointment, name='client_reserve_appointment'),

    # URL path of the form that's used to rescheduled an appointment
    path('client_reschedule_appointment/<int:id>', views.clientRescheduleAppointment, name='client_reschedule_appointment'),

    # URL path of the page that asks client if he is really want to cancel an appointment
    path('client_cancel_appointment/<int:id>', views.clientCancelAppointment, name='client_cancel_appointment'),

    # URL path of the page that asks admin if he is really want to cancel an appointment
    path('admin_cancel_appointment/<int:id>', views.adminCancelAppointment, name='admin_cancel_appointment'),

    # URL path of the form that's used by admin to change/modified appointment data
    path('modify_appointment/<int:id>', views.modifyAppointment, name='modify_appointment'),
    
]