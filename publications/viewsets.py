"""publications API views."""
from rest_framework import viewsets
from rest_framework_gis import filters
from publications.models import Publication,Subscription
from publications.serializers import PublicationSerializer,SubscriptionSerializer


class PublicationViewSet(viewsets.ReadOnlyModelViewSet):
    """publication view set."""
   
    bbox_filter_field = "location"
    filter_backends = (filters.InBBoxFilter,)   
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer

class SubscriptionViewset(viewsets.ModelViewSet):

    bbox_filter_field = "location"
    filter_backends = (filters.InBBoxFilter,)   
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer