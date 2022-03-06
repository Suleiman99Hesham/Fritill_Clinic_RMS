from multiprocessing import context
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import admin_only, unauthenticated_user, allowed_users
from .forms import createUserForm, clientReserveAppointmentForm, modifyAppointmentForm
from django.contrib.auth.models import Group, User
from django.contrib import messages
from .models import Appointment, Client
from .filters import appointmentFilter

# Create your views here.


# mutual views between Clients and Admins

# View the Signup page
# (@unauthenticated_user) Prevent authenticad user to access signup page
@unauthenticated_user
def register(request):
    form = createUserForm()
    if request.method == 'POST':
        form = createUserForm(request.POST)
        if form.is_valid():
            my_group = Group.objects.get_or_create(
                name = 'Client'
                )[0]
            username = form.cleaned_data.get('username')
            user = form.save()
            user = User.objects.get(
                username = username
                )
            user.groups.add(my_group)
            messages.success(
                request, 
                'Account is created successfully for '
                + username
                )
            return redirect('login')
    context = {
        'form': form
        }
    return render(request, 'backend/register.html', context)


# View the Login page 
# (@unauthenticated_user) Prevent authenticad user to access login page
@unauthenticated_user
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request, 
            username = username, 
            password = password
            )
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.info(
                request, 
                'Username OR Password is incorrect'
                )
    context = {}
    return render(request, 'backend/login.html', context)


# Logout a user and redirect to Login page
# (@login_required) Prevent un-authenticad user to make logout request
@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


#-----------------------------------------------------------------------------------


# Views of admins

# View the admin dashboard 
# (@login_required) Prevent un-authenticad user to make logout request
# (admin_only) Prevent clients to access admin dashboard
@login_required(login_url='login')
@admin_only
def adminDashboard(request):
    clients = Client.objects.all()
    last_appointments = Appointment.objects.select_related('client__user').all().order_by('status','-date_created')[0:5]
    context = {
        'clients': clients,
        'last_appointments': last_appointments,
    }
    return render(request, 'backend/admin_dashboard.html', context)


# View all appointments
# (@login_required) Prevent un-authenticad user to make logout request
# (admin_only) Prevent clients to access admin dashboard
@login_required(login_url='login')
@admin_only
def allAppointments(request):
    appoinments = Appointment.objects.all().order_by('status','-date_created')
    myFilter = appointmentFilter(request.GET,queryset = Appointment.objects.all())
    appoinments=myFilter.qs
    context = {
        'appointments': appoinments,
        'myFilter': myFilter,
    }
    return render(request, 'backend/all_appointments.html', context)


# View past appointments
# (@login_required) Prevent un-authenticad user to make logout request
# (admin_only) Prevent clients to access admin dashboard
@login_required(login_url='login')
@admin_only
def pastAppointments(request):
    past_appointments = Appointment.objects.all().filter(status='Passed')
    context = {
        'appointments': past_appointments,
    }
    return render(request, 'backend/specific_appoinments.html', context)


# View upcoming appointments
# (@login_required) Prevent un-authenticad user to make logout request
# (admin_only) Prevent clients to access admin dashboard
@login_required(login_url='login')
@admin_only
def upcomingAppointments(request):
    upcoming_appointments = Appointment.objects.all().filter(status='New').order_by('-date_created')
    context = {
        'appointments': upcoming_appointments,
    }
    return render(request, 'backend/specific_appoinments.html', context)


# View rescheduled appointments
# (@login_required) Prevent un-authenticad user to make logout request
# (admin_only) Prevent clients to access admin dashboard
@login_required(login_url='login')
@admin_only
def rescheduledAppointments(request):
    upcoming_appointments = Appointment.objects.all().filter(status='Rescheduled')
    context = {
        'appointments': upcoming_appointments,
    }
    return render(request, 'backend/specific_appoinments.html', context)


# View the page that asks admin if he really wants to cancel an appointment
# (@login_required) Prevent un-authenticad user to make logout request
# (admin_only) Prevent clients to access admin dashboard
@login_required(login_url='login')
@admin_only
def adminCancelAppointment(request, id):
    appointment = Appointment.objects.get(id=id)
    if request.method == "POST":
        appointment.delete()
        return redirect('admin_dashboard')
    context={
        'appointment': appointment
    }
    return render(request, 'backend/admin_cancel_appointment.html', context)


# View a appointment form that allows admin to update appointment (approved, missed, finished)
# (@login_required) Prevent un-authenticad user to make logout request
# (admin_only) Prevent clients to access admin dashboard
@login_required(login_url='login')
@admin_only
def modifyAppointment(request, id):
    appointment = Appointment.objects.get(id=id)
    form = modifyAppointmentForm(instance=appointment)
    if request.method == 'POST':
        form = modifyAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            approved = form.cleaned_data['approved'] 
            if approved == True:
                appointment.status = 'New'
            form.save()
        return redirect('admin_dashboard')
    context ={
        'form' : form
    }
    return render(request, 'backend/modify_appointment.html', context)


#-----------------------------------------------------------------------------------


# Views of Clients


# View the client dashboard
# (@login_required) Prevent un-authenticad user to make logout request
# (allowed_users) only users that thier group listed in (allowed_roles)
# would be able to access this view
@login_required(login_url='login')
@allowed_users(allowed_roles=['Client'])
def clientDashboard(request, name):
    appointments = request.user.client.appointment_set.all().order_by('-date_created')
    context = {
        'appointments': appointments,
    }
    return render(request, 'backend/client_dashboard.html', context)


# View the appointment reservation form for client 
# (@login_required) Prevent un-authenticad user to make logout request
# (allowed_users) only users that thier group listed in (allowed_roles)
# would be able to access this view
@login_required(login_url='login')
@allowed_users(allowed_roles=['Client'])
def clientReserveAppointment(request):
    client = request.user.client
    form = clientReserveAppointmentForm()
    if request.method == 'POST':
        form = clientReserveAppointmentForm(request.POST)
        if form.is_valid():
            reservation_date = form.cleaned_data['reservation_date']
            new_appointment = form.save(commit=False)
            new_appointment.date = reservation_date
            new_appointment.status = 'New'
            new_appointment.client = client
            new_appointment.save()
            return redirect('client_dashboard', request.user.client.name)
    context = {
        'form' : form,
    }
    return render(request, 'backend/client_reserve_appointment.html', context)


# View the appointment reservation form for client to reschedule an appointment
# (@login_required) Prevent un-authenticad user to make logout request
# (allowed_users) only users that thier group listed in (allowed_roles)
# would be able to access this view
@login_required(login_url='login')
@allowed_users(allowed_roles=['Client'])
def clientRescheduleAppointment(request, id):
    appointment = Appointment.objects.get(id=id)
    form = clientReserveAppointmentForm(instance = appointment)
    if request.method == 'POST':
        form = clientReserveAppointmentForm(request.POST, instance = appointment)
        if form.is_valid():
            print("happened")
            new_reservation_date = form.cleaned_data['reservation_date']
            reschedule_appointment = form.save(commit=False)
            reschedule_appointment.date = new_reservation_date
            reschedule_appointment.status = 'Rescheduled'
            reschedule_appointment.approved = False
            form.save()
        return redirect('client_dashboard' ,appointment.client.name)
    context ={
        'form' : form
    }
    return render(request, 'backend/client_reserve_appointment.html', context)


# View the page that asks client if he really wants to cancel an appointment
# (@login_required) Prevent un-authenticad user to make logout request
# (allowed_users) only users that thier group listed in (allowed_roles)
# would be able to access this view
@login_required(login_url='login')
@allowed_users(allowed_roles=['Client'])
def clientCancelAppointment(request, id):
    appointment = Appointment.objects.get(id=id)
    if request.method == "POST":
        appointment.delete()
        return redirect('client_dashboard' ,appointment.client.name)
    context={
        'appointment' : appointment
    }
    return render(request, 'backend/client_cancel_appointment.html', context)

