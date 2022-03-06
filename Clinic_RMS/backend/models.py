from datetime import date
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Client(models.Model):
    user = models.OneToOneField(User, null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=254, null=True)
    date_created  = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.name

class Appointment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Rescheduled', 'Rescheduled'),
        ('Passed', 'Passed'),
    )

    client = models.ForeignKey(Client,null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    missed = models.BooleanField(default=False, blank=True, null= True)
    finished = models.BooleanField(default=False, blank=True, null= True)
    approved = models.BooleanField(default=False, blank=True, null= True)
    date_created  = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(default='New', max_length=200, null=True, choices=STATUS)
    def __str__(self):
        return '{}\'s appointment'.format(self.client.name)