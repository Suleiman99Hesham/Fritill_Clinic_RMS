from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Get all possible routs by typing http://127.0.0.1:8000/api/
    path('',views.getRoutes),

    #--------------------------------------------------------------------------

    # Get a JWT token for a client to authenticate given his username and password
    # in the request body
    # it returns access and refresh tokens
    # acually it's the login endpoint
    path('GetToken/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Refresh you token for client as access token being expired after five minutes
    # It takes the refresh token in the request body
    # It returns a new access and refresh tokens
    path('GetToken/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #--------------------------------------------------------------------------

    # Appointments endpoints (to request through all appointments endpoints 
    # you have to be authenticated)
    
    # Get all appointments by an admin (only admin allowed)
    path('getAllAppointments/', views.getAllAppointments),

    # Get an appointment based on it's id
    path('getAppointmentsById/<int:id>/', views.getAppointmentsById),

    # Get all appointments of a client given his id (only admin allowed)
    path('getAppointmentsByClient_admin/<int:id>/', views.getAppointmentsByClient_admin),

    # Get all your appointments as a client 
    path('getApointmentsByClient/', views.getApointmentsByClient),

    # Create an appointment given the date in the request body
    path('createAppointment/', views.createAppointment),

    # Update an appointment given the appointment id in the request body
    path('updateAppointment/<int:id>/', views.updateAppointment),

    # Delete an appointment given it's id (only admin allowed)
    path('deleteAppointment/<int:id>/', views.deleteAppointment),

    #--------------------------------------------------------------------------
    
    # Client endpoints (to request through all Client endpoints 
    # you have to be authenticated but only createClient)

    # Get all clients of the system (only admin allowed)
    path('getAllClients/', views.getAllClients),

    # Get client data given his id
    path('getClientById/<int:id>/', views.clientById),

    # Create a client given his (name, email, password)[required] in the request body
    # (actually it's the registeration endpoint )
    path('createClient/', views.clientCreate),

    # Update a client data given his id and the new data in the request body (admin only)
    path('updateClient/<int:id>/', views.clientUpdate),

    # Delete a client given his id (admin only)
    path('deleteClient/<int:id>/', views.clientDelete),
]
