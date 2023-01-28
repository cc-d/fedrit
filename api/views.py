from django.contrib.auth import authenticate, login, logout
from django_typomatic import ts_interface, get_ts, generate_ts
from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .models import PlatformUser, Platform
from .serializers import PlatformUserSerializer

import logging
logger = logging.getLogger(__name__)

class LoginView:
    permission_classes = (AllowAny)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        serializer = PlatformUserSerializer(data=request.data)
        validated_data = serializer.validated_data

        if serializer.is_valid():
            user = authenticate(
                username=validated_data['username'],
                password=validated_data['password'])
            if user:
                token = Token.objects.get_or_create(user=user)
                return Response({'success': 'ok', 'token': token.key})
            else:
                return Response(
                    {'error': 'Invalid Credentials'}, 
                    status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
