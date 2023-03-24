from rest_framework import generics
from json import loads, dumps
from api.serializers import CommunitySerializer
from copy import deepcopy
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
from models import (
    PlatformUser, Platform, Community, host_platform, Post,
    Comment, UserToken
)
from serializers import (
    PlatformUserSerializer, CommunitySerializer, PostSerializer,
    CommentSerializer, UserTokenSerializer,
)

import logging
logger = logging.getLogger(__name__)

class AuthViewSet(viewsets.ModelViewSet):
    queryset = PlatformUser.objects.all()
    serializer_class = PlatformUserSerializer

    def get_permissions(self):
        if self.action in ['logout']:
            return [AllowAny()]
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
        try:
            request.user.auth_token.delete()
        except AttributeError as e:
            pass
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
        if 'name' in kwargs:
            kwargs['comm']
        print('postargskargs', args, kwargs)
        serializer = self.get_serializer(data=request.data, context=kwargs)
        print('afterser', serializer)
        serializer.is_valid(raise_exception=True)
        print('isvalid', serializer)
        vdata = serializer.validated_data
        print('vdata',vdata)

        cposts = Post.objects.filter(community__id=vdata.id).all() or []
        return Response([PostSerializer(p).data for p in cposts])


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    @action(methods=['POST'], detail=False)
    def create_post(self, request):
        context = {
            'community_id': request.data.get('community_id', None),
            'community_name': request.data.get('community_name', None),
            'author': request.user,
            'platform': host_platform()
        }

        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        vdata = serializer.validated_data
        author = request.user

        newpost = Post.objects.create(
            title=vdata['title'], text=vdata['text'],
            platform=host_platform(), community=vdata['community'],
            author=author)
        return Response(PostSerializer(newpost).data)

    @action(methods=['GET'], detail=False)
    def comments(self, request, **kwargs):
        print('ddddddd',request)
        serializer = CommentSerializer(data=request.data, context=kwargs)
        serializer.is_valid(raise_exception=True)
        vdata = serializer.validated_data
        return Response({
            'post': PostSerializer(vdata['post']).data,
            'comments': [CommentSerializer(c).data for c in vdata['comments']],
        })

    @action(methods=['GET'], detail=False)
    def all(self, request):
        posts = list(Post.objects.all())
        posts = [PostSerializer(p).data for p in posts]
        return Response(posts)


class UserTokenViewSet(viewsets.ModelViewSet):
    queryset = UserToken.objects.all()
    serializer_class = UserTokenSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


