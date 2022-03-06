from rest_framework.serializers import ModelSerializer
from rest_framework import validators
from backend.models import Appointment, Client
from django.contrib.auth.models import User

# Serialize appointment data to be able to return it as json objects
class AppointmentSerializer(ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

# Serialize Client data to be able to return it as json objects
class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

# Serialize user data to be able to save it then create a client object of this data  
class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

        extra_kwargs = {
            'password':{'write_only': True},
            'email':{
                'required':True,
                'allow_blank': False,
                'validators':{
                    validators.UniqueValidator(
                        User.objects.all(), 'A user with that email already exists'
                    )
                }
            }
        }
    
    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        email = validated_data.get('email')
        
        user = User.objects.create(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()
        Client.objects.create(
            user = user,
            name = username,
            email = email
        )

        return user
