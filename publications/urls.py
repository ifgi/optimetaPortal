"""publications urls."""

from django.urls import path,include
from publications.views import successView,privacypolicy,Confirmationlogin,loginres,optimap,autheticate_via_magic_link,customlogout,user_settings,user_subscriptions,delete_account,change_useremail,harvest_data
from .feeds import OptimetaFeed
from .feeds import atomFeed
from sesame.views import LoginView

app_name = "publications"

urlpatterns = [
    
    path("api/", include("publications.api")), 
    # RSS route 
    path(r'feed/rss', OptimetaFeed(), name ="GeoRSSfeed"), 
    path("feed/atom", atomFeed(), name ="GeoAtomfeed"),
    path("success/",successView,name="success"),
    path("login/auth/", LoginView.as_view(), name="login"),
    path('',optimap,name="optimap"),
    path("loginres/",loginres,name="loginres"),
    path("privacy/",privacypolicy,name="privacy"),
    path("loginconfirm/",Confirmationlogin,name="loginconfirm"),
    path("<str:token>", autheticate_via_magic_link, name="magic_link"),
    path("logout/", customlogout, name="logout"),
    path("usersettings/", user_settings, name ="usersettings"),
    path("subscriptions/", user_subscriptions, name ="subscriptions"),
    path("delete/", delete_account, name ="delete"),
	path("changeuser/", change_useremail, name ="changeuser"),
	path("harvest/", harvest_data, name ="harvest"),
]



#path('map/marker/<int:pk>', MarkerCreate.as_view(), name='retrieve-customer'),import requests
