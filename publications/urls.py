"""publications urls."""

from django.urls import path,include

from publications.views import PublicationsMapView, EmailLoginView, successView
from .feeds import OptimetaFeed
from .feeds import atomFeed
from sesame.views import LoginView

app_name = "publications"

urlpatterns = [

    path("map/", PublicationsMapView.as_view()),
    path("api/", include("publications.api")), 
    # RSS route 
    path(r'feed/rss', OptimetaFeed(), name ="GeoRSSfeed"), 
    path("feed/atom", atomFeed(), name ="GeoAtomfeed"),
    path("success/",successView, name="success"),
    path('login/',EmailLoginView, name="email_login"),
    path("login/auth/", LoginView.as_view(), name="login"),
]



#path('map/marker/<int:pk>', MarkerCreate.as_view(), name='retrieve-customer'),import requests
