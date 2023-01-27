"""publications serializers."""

from rest_framework_gis import serializers
from .models import Publication

from publications.models import Publication,Subscription

class PublicationSerializer(serializers.GeoFeatureModelSerializer):
    """publication GeoJSON serializer."""

    class Meta:
        """publication serializer meta class."""
        model = Publication
        fields = ("id", "title" ,"abstract", "publicationDate", "url", "doi","creationDate", "lastUpdate","timeperiod_startdate","timeperiod_enddate")
        geo_field = "geometry"
        auto_bbox = True      
       
class SubscriptionSerializer(serializers.GeoFeatureModelSerializer):
    """Subscription GeoJSON serializer."""

    class Meta:
        model = Subscription
        fields = ("search_text","timeperiod_startdate","timeperiod_enddate","user_name")
        geo_field = "search_area"
        auto_bbox = True
        