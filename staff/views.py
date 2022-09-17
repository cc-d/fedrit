from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def home(request):
    return HttpResponse('Staff')
