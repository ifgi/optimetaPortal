from django.contrib.gis.db import models
from publications.models import publication
from django.contrib.gis import geos
from django.contrib.gis.geos import GEOSGeometry,Polygon,MultiPolygon
#polygon = GEOSGeometry('POLYGON ((-98.503358 29.335668, -98.503086 29.335668, -98.503086 29.335423, -98.503358 29.335423, -98.503358 29.335668))', srid=4326)


polygon1 = GEOSGeometry('POLYGON((102.0 2.0,103.0 2.0,103.0 3.0,102.0 3.0,102.0 2.0))',srid=4326)
polygon2 = GEOSGeometry('POLYGON((100.0 0.0,101.0 0.0,101.0 1.0,100.0 1.0,100.0 0.0))',srid=4326)
mp = GEOSGeometry('MULTIPOLYGON(polygon1,polygon2)')

p1 = Polygon( ((102.0, 2.0),(103.0 ,2.0),(103.0, 3.0),(102.0, 3.0),(102.0, 2.0)) )
p2 = Polygon(((100.0,0.0),(101.0, 0.0),(101.0,1.0),(100.0,1.0),(100.0,0.0)))
         
bounds=MultiPolygon([Polygon(((-117.869537353516, 33.5993881225586),(-117.869537353516, 33.7736549377441),(-117.678024291992, 33.7736549377441),(-117.678024291992, 33.5993881225586),(-117.869537353516, 33.5993881225586)))])
publication = publication(id = 1, name='iceland', location=bounds)
publication.save()