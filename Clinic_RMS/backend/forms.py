from dataclasses import fields
from django.forms import ModelForm, DateTimeField
from datetime import timezone, datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Client, Appointment

class createUserForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# A form uses to reserve appointments
class clientReserveAppointmentForm(ModelForm):
    reservation_date = DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    class Meta:
        model = Appointment
        fields=[]

    # Check if the taken date is in the future ( > the time of the moment he enter it) 
    def clean(self):
        cd = self.cleaned_data
        app_date = cd.get('reservation_date').date()
        app_date_hour =  cd.get('reservation_date').time().hour
        today_date = datetime.now(timezone.utc).date()
        today_date_hour =  datetime.now(timezone.utc).time().hour +2
        
        if (app_date < today_date) or (app_date == today_date and app_date_hour < today_date_hour):
            raise ValidationError("Reservation Date must be in the future!")
        
        return cd


# A form uses to update the appointmment
class modifyAppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields=['approved', 'missed', 'finished']