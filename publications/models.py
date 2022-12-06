from django.db import models
"""Markers models."""

from django.contrib.gis.db import models
from datetime import date,timedelta


class Publication(models.Model):
    """A scientific publication with a title and location."""

    title = models.CharField(max_length=4096)
    abstract = models.TextField()
    publicationDate = models.DateField()
    doi = models.CharField(max_length=1024, null=True)
    url = models.URLField(max_length=1024, null=True)
    geometry = models.GeometryCollectionField()
    journal = models.CharField(max_length=1024, null=True)

    creationDate = models.DateTimeField(auto_now_add=True)
    lastUpdate = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return string representation."""
        return self.title


class OJSservers(models.Model):

    url_field = models.URLField(max_length = 200)
    Harvest_Interval = models.DurationField(default=timedelta)
    Last_Harvest = models.DateTimeField(auto_now_add=True,null=True)
    