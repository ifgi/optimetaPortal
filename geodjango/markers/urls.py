"""Markers urls."""

from django.urls import path,include

from markers.views import MarkersMapView

app_name = "markers"

urlpatterns = [
    path("map/", MarkersMapView.as_view()),
    path("api/", include("markers.api")),   
]

#path('map/marker/<int:pk>', MarkerCreate.as_view(), name='retrieve-customer'),