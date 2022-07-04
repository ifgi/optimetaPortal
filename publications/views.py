from django.shortcuts import render
from django.views.generic.base import TemplateView
from publications.models import Publication
from rest_framework import generics
from publications.serializers import PublicationSerializer
from django.core import serializers

class PublicationsMapView(TemplateView):
    """publications map view."""

    template_name = "map.html"

#class MarkerCreate(generics.RetrieveAPIView):
    # API endpoint that allows return of muiltipolygon
    #queryset = serializers.serialize("json", Marker.objects.all()),
    #serializer_class = publicationserializer

