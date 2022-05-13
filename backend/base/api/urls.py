from django.urls import path
from . import views
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [


    path('notes/', views.getNotes),

    path('',views.getRoutes,name='GetRoutes'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', views.userSignup, name='Signup'),
    path('adduser/', views.addUser, name='AddUser'),
    path('getusers/', views.getUsers, name='GetUsers'),
    path('updateuser/', views.updateUser, name='UpdateUser'),
    path('userdetails/', views.getUserDetails, name='UserDetails'),
    path('deleteuser/', views.deleteUser, name='DeleteUser'),
    path('isadmin/', views.isAdmin, name='IsAdmin'),
    path('createNotes/',views.createNotes, name='CreateNotes'),
]
