from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField


class Publication(models.Model):
          
    title = models.CharField(max_length=4096,null =True)
    abstract = models.TextField(null=True)
    publicationDate = models.DateField(null=True)
    doi = models.CharField(max_length=1024, null=True)
    url = models.URLField(max_length=1024, null=True)
    geometry = models.GeometryCollectionField(verbose_name='Publication geometry (Points, Lines, Polygons as GeoJSON)',srid = 4326, null=True, blank=True)
    journal = models.CharField(max_length=1024, null=True)
    creationDate = models.DateTimeField(auto_now_add=True,null=True)
    lastUpdate = models.DateTimeField(auto_now=True,null=True)
    timeperiod_startdate = ArrayField(models.DateField(null=True), null=True)
    timeperiod_enddate = ArrayField(models.DateField(null=True), null=True)

    def __str__(self):
        """Return string representation."""
        return self.title

class OJSservers(models.Model):

    url_field = models.URLField(max_length = 200)
    harvest_interval_minutes = models.IntegerField(default=60*24*3)
    last_harvest = models.DateTimeField(auto_now_add=True,null=True)
    
class Subscription(models.Model):
    name = models.CharField(max_length=4096)
    timeperiod_startdate = models.DateField(null=True)
    timeperiod_enddate = models.DateField(null=True)
    search_area = models.GeometryCollectionField(null=True, blank=True)
    user_name = models.CharField(max_length=4096)

    def __str__(self):
        """Return string representation."""
        return self.name

    class Meta:
        ordering = ['user_name']
        verbose_name = "subscription"