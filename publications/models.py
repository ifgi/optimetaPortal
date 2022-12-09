from django.db import models
"""Markers models."""

from django.contrib.gis.db import models



class Publication(models.Model):
    """A marker with name and location."""
       
    title = models.CharField(max_length=4096)
    abstract = models.TextField( null=True)
    publicationDate = models.DateField(auto_now_add=True)
    doi = models.CharField(max_length=1024, null=True)
    url = models.URLField(max_length=1024, null=True)
    geometry = models.GeometryCollectionField(verbose_name='geo',srid = 4326, null=True, blank=True)
    journal = models.CharField(max_length=1024, null=True)
    creationDate = models.DateTimeField(auto_now_add=True,null=True)
    lastUpdate = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        """Return string representation."""
        return self.title

class OJSservers(models.Model):

    url_field = models.URLField(max_length = 200)
    harvest_interval = models.DurationField(null=True)
    last_harvest = models.DateTimeField(auto_now_add=True,null=True)
    