"""Markers API views."""
from rest_framework import viewsets
from rest_framework_gis import filters
from django.core import serializers
from markers.models import Marker
from markers.serializers import MarkerSerializer


class MarkerViewSet(viewsets.ModelViewSet):
    """Marker view set."""

    #queryset = serializers.serialize("json", Marker.objects.all())
    #bbox_filter_field = "location"
    #filter_backends = (filters.InBBoxFilter,)
    
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer
    
    