from django.contrib import admin
"""Markers admin."""

from django.contrib.gis import admin

from publications.models import Publication


@admin.register(Publication)
class PublicationAdmin(admin.OSMGeoAdmin):
    """Publication Admin."""

    list_display = ("name", "location")
# Register your models here.
