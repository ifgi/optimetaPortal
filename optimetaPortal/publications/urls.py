"""publications urls."""

from django.urls import path,include

from publications.views import PublicationsMapView
from .feeds import OptimetaFeed
from .feeds import atomFeed


app_name = "publications"

urlpatterns = [
    path("map/", PublicationsMapView.as_view()),
    path("api/", include("publications.api")), 
    # RSS route 
    path(r'feed/rss', OptimetaFeed(), name ="GeoRSSfeed"), 
    path("feed/atom", atomFeed(), name ="GeoAtomfeed")
]

#path('map/marker/<int:pk>', MarkerCreate.as_view(), name='retrieve-customer'),