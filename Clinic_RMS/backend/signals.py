from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Client

# It creates a client object whenever user object is created
def Client_profile(sender ,instance ,created , **kwargs):
    if created:
        if instance.is_staff:
            group = Group.objects.get_or_create(name='admin')
            instance.groups.add(group[0])
        else:
            group = Group.objects.get_or_create(name='Client')
            instance.groups.add(group[0])
            Client.objects.create(
                    user=instance,
                    name=instance.username,
                    email=instance.email,
                )

post_save.connect(Client_profile, sender=User)