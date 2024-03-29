"""fedrit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import api.views
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers


router = routers.SimpleRouter(trailing_slash=False)
router.register(r'auth', api.views.AuthViewSet)
router.register(r'community', api.views.CommunityViewSet)
router.register(r'post', api.views.PostViewSet)
router.register(r'user-tokens', api.views.PlatUserTokenViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    re_path(r'^api/tokenuser$', api.views.TokenUserView.as_view()),
    re_path(
        r'^api/community/(?P<community_name>[a-zA-Z0-9-_]+)/posts$',
        api.views.CommunityViewSet.as_view({'get': 'posts'})),
    re_path(
        r'^api/post/(?P<post_id>[a-zA-Z0-9-_]+)/comments$',
        api.views.PostViewSet.as_view({'get':'comments'}),
    )
]