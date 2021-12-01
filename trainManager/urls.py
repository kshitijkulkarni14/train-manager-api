"""trainManager URL Configuration"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('api/v1/',include('trainDepartureViewer.api.v1.urls'))
]
