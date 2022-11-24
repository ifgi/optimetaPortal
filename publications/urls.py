"""publications urls."""

from django.urls import path,include
from publications.views import successView,Confirmationlogin,loginres,optimap,privacypolicy,autheticate_via_magic_link,customlogout
from .feeds import OptimetaFeed
from .feeds import atomFeed
from sesame.views import LoginView

app_name = "publications"

urlpatterns = [
    path('',             optimap, name='optimap'),
    path('api/',         include('publications.api')), 
    path('feed/rss',     OptimetaFeed(), name ='GeoRSSfeed'), 
    path('feed/atom',    atomFeed(), name ='GeoAtomfeed'),
    path('success/',     successView,name='success'),
    path('login/auth/',  LoginView.as_view(), name='login'),
    path('loginres/',    loginres,name="loginres"),
    path('privacy',      privacypolicy,name='privacy'),
	path('loginconfirm/',Confirmationlogin,name="loginconfirm"),
	path("<str:token>", autheticate_via_magic_link, name="magic_link"),
	path("logout/", customlogout, name="logout"),											 
]



#path('map/marker/<int:pk>', MarkerCreate.as_view(), name='retrieve-customer'),import requests
