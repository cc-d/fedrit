from rest_framework import generics
from api.serializers import CommunitySerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login, logout
from django_typomatic import ts_interface, get_ts, generate_ts
from django.shortcuts import render
from django.db.utils import IntegrityError
from rest_framework import views, status, viewsets, serializers
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import (
    AllowAny, IsAdminUser, IsAuthenticated, 
)
from rest_framework.decorators import action
from rest_framework.views import APIView
from .models import (
    PlatformUser, Platform, Community, host_platform, Post,
)
from .serializers import (
    PlatformUserSerializer, CommunitySerializer, PostSerializer
)

import logging
logger = logging.getLogger(__name__)

class AuthViewSet(viewsets.ModelViewSet):
    queryset = PlatformUser.objects.all()
    authentication_classes = [TokenAuthentication]
    serializer_class = PlatformUserSerializer

    def get_permissions(self):
        if self.action in ['logout']:
            return [IsAuthenticated()]
        return [AllowAny()]

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
        token = Token.objects.filter(key=token).first()
        if token:
            user = token.user
            user.token = token
            serializer = PlatformUserSerializer(user)
            return Response(serializer.data)
        return Response({'error':'no token found'})


class CommunityViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommunitySerializer
    queryset = Community.objects.all()

    @action(methods=['POST'], detail=False)
    def create_community(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        community = serializer.save()
        return Response(CommunitySerializer(community).data)

    @action(methods=['GET'], detail=False)
    def all(self, request):
        comms = list(Community.objects \
            .filter(platform=host_platform()) \
            .all())
        return Response([CommunitySerializer(c).data for c in comms])

    @action(methods=['GET'], detail=False)
    def posts(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vdata = serializer.validated_data

        cposts = list(
            Post.objects.filter(community_id=vdata['id']).all())
        return Response([PostSerializer(p) for p in cposts])


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    @action(methods=['POST'], detail=False)
    def create_post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vdata = serializer.validated_data
        author = request.user

        newpost = Post(
            title=vdata['title'], text=vdata['text'],
            platform=host_platform(), community=vdata['community'],
            author=author)