"""publications API views."""
from rest_framework import viewsets
from rest_framework_gis import filters
from publications.models import Publication
from publications.serializers import PublicationSerializer


class PublicationViewSet(viewsets.ReadOnlyModelViewSet):
    """publication view set."""

    #queryset = serializers.serialize("json", publication.objects.all())
    bbox_filter_field = "location"
    filter_backends = (filters.InBBoxFilter,)
    
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    
    """def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)"""
    