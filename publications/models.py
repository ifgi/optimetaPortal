from django.db import models
"""Markers models."""

from django.contrib.gis.db import models
from datetime import date


class Publication(models.Model):
    """A scientific publication with a title and location."""

    title = models.CharField(max_length=4096)
    abstract = models.TextField()
    publicationDate = models.DateField()
    doi = models.CharField(max_length=1024, null=True)
    url = models.URLField(max_length=1024, null=True)
    geometry = models.GeometryCollectionField()

    creationDate = models.DateTimeField(auto_now_add=True)
    lastUpdate = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return string representation."""
        return self.title
