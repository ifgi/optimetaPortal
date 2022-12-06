from django.contrib import admin
"""Markers admin."""

from django.contrib.gis import admin

from publications.models import Publication,OJSservers


@admin.register(Publication)
class PublicationAdmin(admin.OSMGeoAdmin):
    """Publication Admin."""

    list_display = ("title", "publicationDate", "creationDate", "lastUpdate")
# Register your models here.

@admin.register(OJSservers)
class ServerAdmin(admin.OSMGeoAdmin):

    url_display = ("url_field","Harvest_Interval","Last_Harvest")