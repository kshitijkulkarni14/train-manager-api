"""trainManager URL Configuration"""

from django.urls import path,include
from trainDepartureViewer.api.v1 import views

urlpatterns = [
    path('trains/', views.get_trains, name='trains'),
    path('stations/', views.get_stations, name='stations'),
    path('api-token/', views.get_api_token, name='api_token')
]
