from django.shortcuts import render
from django.views.generic.base import TemplateView
from markers.models import Marker
from rest_framework import generics
from markers.serializers import MarkerSerializer
from django.core import serializers

class MarkersMapView(TemplateView):
    """Markers map view."""

    template_name = "map.html"

#class MarkerCreate(generics.RetrieveAPIView):
    # API endpoint that allows return of muiltipolygon
    #queryset = serializers.serialize("json", Marker.objects.all()),
    #serializer_class = MarkerSerializer

