from django_filters import FilterSet, DateFilter, CharFilter, NumberFilter
from django import forms

from .models import Appointment

class DateTimeTypeInput(forms.DateInput):
    input_type = 'date'

class appointmentFilter(FilterSet):
    start_date = DateFilter(widget=DateTimeTypeInput(), field_name="date", lookup_expr='date__gte')
    end_date = DateFilter(widget=DateTimeTypeInput(), field_name="date", lookup_expr='date__lte')

    # hours__gte = NumberFilter(field_name='date', lookup_expr='hour__gte')
    # hours__lte = NumberFilter(field_name='date', lookup_expr='hour__lte')

    class Meta:
        model = Appointment
        fields = '__all__'
        exclude = ['date', 'rescheduled_date', 'date_created', 'missed', 'finished']