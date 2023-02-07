from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login, logout
from django_typomatic import ts_interface, get_ts, generate_ts
from django.shortcuts import render
from django.db.utils import IntegrityError
from rest_framework import views, status, viewsets, serializers
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.views import APIView
from .models import PlatformUser, Platform
from .serializers import PlatformUserSerializer

import logging
logger = logging.getLogger(__name__)

class AuthViewSet(viewsets.ModelViewSet):
    queryset = PlatformUser.objects.all()
    serializer_class = PlatformUserSerializer

    def get_permissions(self):
        if self.action in ['login', 'register']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(methods=['POST'], detail=False)
    def login(self, request):
        user = authenticate(
            username=request.data['username'],
            password=request.data['password'])
        if user:
            token = Token.objects.get_or_create(user=user)[0]
            return Response({'token': token.key})
        else:
            return Response(
                {'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['POST'], detail=False)
    def logout(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            user, utoken = serializer.create(validated_data, return_token=True)
        except IntegrityError as ie:
            return Response({'error':'user already exists'})

        return Response({'user':PlatformUserSerializer(user).data, 'token':utoken.key})


class TokenUserView(APIView):
    """
    Determine the current user by their token, and return their data
    """
    def post(self, request):
        token = request.data.get('token', None)
        user = Token.objects.filter(key=token).first().user
        user.token = token
        serializer = PlatformUserSerializer(user)
        return Response(serializer.data)
