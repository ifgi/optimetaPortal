from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from publications.models import Publication

@admin.register(Publication)
class PublicationAdmin(LeafletGeoAdmin):
    """Publication Admin."""

    list_display = ("title", "publicationDate", "creationDate", "lastUpdate")
