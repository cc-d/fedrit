from rest_framework import viewsets, permissions
from .serializers import *
from django.shortcuts import render

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerial
    permission_classes = []#permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerial
    permission_classes = [permissions.IsAuthenticated]
