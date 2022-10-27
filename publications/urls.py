"""publications urls."""

from django.urls import path,include
from publications.views import PublicationsMapView,EmailloginView,successView,PublicationsTimelineView,Confirmationlogin,loginres,optimap,privacypolicy
from .feeds import OptimetaFeed
from .feeds import atomFeed
from sesame.views import LoginView

app_name = "publications"

urlpatterns = [
    path('',             optimap, name='optimap'),
    path('map/',         PublicationsMapView.as_view()),
    path('api/',         include('publications.api')), 
    path('feed/rss',     OptimetaFeed(), name ='GeoRSSfeed'), 
    path('feed/atom',    atomFeed(), name ='GeoAtomfeed'),
    path('success/',     successView,name='success'),
    path('login/',       EmailloginView,name='email_login'),
    path('login/auth/',  LoginView.as_view(), name='login'),
    path('timeline/',    PublicationsTimelineView.as_view()),
    path('loginres/',    loginres,name="loginres"),
    path('privacy',      privacypolicy,name='privacy'),
	path('loginconfirm/',Confirmationlogin,name="loginconfirm"),
]



#path('map/marker/<int:pk>', MarkerCreate.as_view(), name='retrieve-customer'),import requests
