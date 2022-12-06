"""publications urls."""

from django.urls import path,include
from publications.views import privacypolicy,Confirmationlogin,loginres,optimap,autheticate_via_magic_link,customlogout,user_settings,user_subscriptions,delete_account,change_useremail
from .feeds import OptimetaFeed
from .feeds import atomFeed


app_name = "publications"

urlpatterns = [
    
    path("api/", include("publications.api")), 
    # RSS route 
    path(r'feed/rss', OptimetaFeed(), name ="GeoRSSfeed"), 
    path("feed/atom", atomFeed(), name ="GeoAtomfeed"),
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
	
]




