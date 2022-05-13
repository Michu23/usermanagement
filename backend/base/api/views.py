

from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


from .serializers import *
from base.models import Note

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]

    return Response(routes)



# @permission_classes([IsAuthenticated])
@api_view(['GET'])
def getNotes(request):
    notes = Note.objects.all()
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createNotes(request):
    user=request.user
    notes= request.data['notes']
    Note.objects.create(user=user,body=notes)
    # noteslist = Note.objects.create(user=user,body=notes)
    # noteslist.save()
    return Response({'status': True})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getUsers(request):
    if request.user.is_staff:
        users = User.objects.all()
        usersList = []
        for user in users:
            if user.is_staff == False:
                usersList.append({
                    'id': user.id,
                    'name': user.first_name,
                    'username': user.username,
                    'password': user.password,
                })

        print(usersList)
        return Response({'status': True, 'data':usersList})
    # else:
    #     return Response({'status': False, 'error': 'You are not authorized to view details of users'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteUser(request):
    if request.user.is_staff:
        User.objects.filter(id=request.data['id']).delete()
        users = User.objects.all()
        usersList = []
        for user in users:
            if user.is_staff == False:
                usersList.append({
                    'id': user.id,
                    'name': user.first_name,
                    'username': user.username,
                    'password': user.password,
                })
        return Response({'status': True, 'data':usersList})
    # else:
    #     return Response({'status': False, 'error': 'You are not authorized to delete users'})



@api_view(['POST'])
def userSignup(request):
    name = request.data['name']
    username = request.data['username']
    password = request.data['password'] 
    try:
        User.objects.get(username=username)
        return Response({'status': False})
    except:
        user = User.objects.create_user(first_name=name, username=username, password=password)
        user.save()
        return Response({'status': True, 'message': 'Account created successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addUser(request):
    if request.user.is_staff:
        name = request.data['name']
        username = request.data['username']
        password = request.data['password']
        user = User.objects.create_user(first_name=name, username=username, password=password)
        user.save()
        return Response({'status': True, 'message': 'User added successfully'})
    else:
        return Response({'status': False, 'error': 'You are not authorized to add users'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateUser(request):
    if request.user.is_staff:
        # try:
        #     User.objects.get(username=request.data['username'])
        #     return Response({'status': False, 'error': 'Username already exists'})
        # except:
        User.objects.filter(id=request.data['id']).update(first_name=request.data['name'], username=request.data['username'])
        return Response({'status': True, 'message': 'User updated successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getUserDetails(request):
    if request.user.is_staff:
        user = User.objects.get(id=request.data['id'])
        return Response({'status': True, 'data': {
            'id': user.id,
            'name': user.first_name,
            'username': user.username,
        }})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def isAdmin(request):
    if request.user.is_staff:
        return Response({'status': True})
    else:
        return Response({'status': False})


