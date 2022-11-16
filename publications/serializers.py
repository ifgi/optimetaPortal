"""publications serializers."""

from rest_framework_gis import serializers
from .models import Publication

from publications.models import Publication


class PublicationSerializer(serializers.GeoFeatureModelSerializer):
    """publication GeoJSON serializer."""

    class Meta:
        """publication serializer meta class."""
        model = Publication
        #fields = ("id", "name" ,"date")
        fields = ("title" ,"abstract", "publicationDate", "url", "doi")
        geo_field = "geometry"
        auto_bbox = True      
       
        
        
        