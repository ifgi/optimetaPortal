from django.contrib.gis.feeds  import Feed
from .models import Publication
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed,Rss201rev2Feed
import django.utils.feedgenerator as feedgenerator
class OptimetaFeed(Feed):
    title = "Latest blog"
    link = ""
    description = "Latest blog posts"
	
    feed_type = Rss201rev2Feed
    
    def geometry(self):
        # Can also return: `obj.poly`, and `obj.poly.centroid`.
        return Publication.objects# tuple like: (X0, Y0, X1, Y1).        
	
    def item_title(self, item):
        return item.title 
        
class atomFeed(Feed):
    feed_type = Atom1Feed

