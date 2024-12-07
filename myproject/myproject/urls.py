from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import redirect

from django.views.generic import TemplateView



def home(request):
    return HttpResponse("Welcome to the Toll Tracking System API!")




urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', home),
   
]
