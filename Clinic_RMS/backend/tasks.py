from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from datetime import datetime, timezone
from .models import Appointment
# current_time = now.strftime("%H:%M:%S")

from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# Return hours of timedelta
def hours(td):
    return td.days, td.seconds//3600, (td.seconds//60)%60


@shared_task(name = "send_mail")
def schedule_mail():

    # Rendered this template if remainig time is 24
    message_24 = render_to_string('backend/schedule_mail_24.html')
    mail_subject_24 = 'there is 1 Day left to your appointment'

    # Rendered this template if remainig time is 6
    message_6 = render_to_string('backend/schedule_mail_6.html')
    mail_subject_6 = 'there is 1 Day left to your appointment'

    # Rendered this template if the appointment starts now
    message_0 = render_to_string('backend/schedule_mail_0.html')
    mail_subject_0 = 'there is 1 Day left to your appointment'

    appointments = Appointment.objects.all().filter(
        status = "New",
        approved = True,
        )
    for appointment in appointments:
        diff = appointment.date-datetime.now(timezone.utc)
        diff_hours = hours(diff)
        remaining_hours = diff_hours +2
        if (remaining_hours == 24):
            to_email = appointment.client.email
            email = EmailMessage(
                mail_subject_24, 
                message_24, 
                to=[to_email]
                )
            email.send()
        elif (remaining_hours == 6):
            to_email = appointment.client.email
            email = EmailMessage(
                mail_subject_6, 
                message_6, 
                to=[to_email]
                )
            email.send()
        elif (remaining_hours == 0):
            to_email = appointment.client.email
            email = EmailMessage(mail_subject_0, 
            message_0, 
            to=[to_email]
            )
            email.send()