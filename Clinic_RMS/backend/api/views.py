from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.models import Group, User
from .serializers import AppointmentSerializer, ClientSerializer, RegisterSerializer
from backend.models import Appointment, Client



# The responsible serializer of user authentication
# I customized it to return the username and group of user not just the id
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['groub'] = Group.objects.get(user=user).name

        return token


# Get a JWT token for a client to authenticate given his username and password
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Get all possible routs by typing http://127.0.0.1:8000/api/
@api_view(['GET'])
def getRoutes(request):

    routes=[
        ##token endpoints 

        'api/GetToken/', 
        'api/GetToken/refresh/',

        #appointments endpoints
        'api/getAllAppointments/',
        'api/getAppointmentsById/<int:id>/',
        'api/getAppointmentsByClient_admin/<int:id>/',
        'api/getApointmentsByClient/',
        'api/createAppointment/',
        'api/updateAppointment/<int:id>/',
        'api/deleteAppointment/<int:id>/',
        
        #client endpoints
        'api/getAllClients/',
        'api/getClientById/<int:id>/',
        'api/createClient/',
        'api/updateClient/<int:id>/',
        'api/deleteClient/<int:id>/',
    ]
    return Response(routes)


# Get all appointments by an admin (only admin allowed)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def getAllAppointments(request):

    appointments = Appointment.objects.all()
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


# Get an appointment based on it's id
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAppointmentsById(request, id):

    appointments = Appointment.objects.get(id=id)
    serializer = AppointmentSerializer(appointments, many=False)
    return Response(serializer.data)


# Get all appointments of a client given his id (only admin allowed)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def getAppointmentsByClient_admin(request, id):

    client = Client.objects.get(id=id)
    appointments = client.appointment_set.all()
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


# Get all your appointments as a client
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getApointmentsByClient(request):

    client = Client.objects.get(user=request.user)
    appointments = client.appointment_set.all()
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


# Create an appointment given the date in the request body
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createAppointment(request):

    client = Client.objects.get(user=request.user)
    serializer = AppointmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data['client'] = client
        serializer.save()
    return Response(serializer.data)


# Update an appointment given the date
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateAppointment(request, id):

    appointment = Appointment.objects.get(id=id)
    serializer = AppointmentSerializer(instance=appointment,data=request.data)
    if serializer.is_valid():
        serializer.validated_data['approved'] = False
        serializer.save()
    return Response(serializer.data)


# Delete an appointment given it's id (only admin allowed)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def deleteAppointment(request, id):

    appointment = Appointment.objects.get(id=id)
    appointment.delete()
    return Response("item successfully deleted!")


# Get all clients
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def getAllClients(request):

    clients = Client.objects.all()
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)


# Get client data given his id
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def clientById(request, id):

    client = Client.objects.get(id=id)
    serializer = ClientSerializer(client, many=False)
    return Response(serializer.data)


# Create a client
@api_view(['POST'])
def clientCreate(request):

    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
    return Response(serializer.data)


# Update a client data given his id
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def clientUpdate(request, id):

    client = Client.objects.get(id=id)
    serializer = ClientSerializer(instance=client,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


# Delete a client given his id
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def clientDelete(request, id):

    client = Client.objects.get(id=id)
    client.delete()
    return Response("Client successfully deleted!")


