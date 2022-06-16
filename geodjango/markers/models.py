from django.db import models
"""Markers models."""

from django.contrib.gis.db import models


class Marker(models.Model):
    """A marker with name and location."""

    name = models.CharField(max_length=255)
    location = models.MultiPolygonField()

    def __str__(self):
        """Return string representation."""
        return self.name
# Create your models here.
