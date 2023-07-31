"""OPTIMAP urls."""

from django.urls import path,include
from django.shortcuts import redirect
from publications.views import privacypolicy,Confirmationlogin,loginres,optimap,autheticate_via_magic_link,customlogout,user_settings,user_subscriptions,delete_account,change_useremail,data,add_subscriptions
from .feeds import OptimetaFeed
from .feeds import atomFeed
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

app_name = "optimap"

urlpatterns = [
    path('', optimap, name="home"),
    path('favicon.ico', lambda request: redirect('static/favicon.ico', permanent=True)),
    path("api", lambda request: redirect('/api/v1/', permanent=False)),
    path("api/", lambda request: redirect('/api/v1/', permanent=False)),
    path("api/v1", lambda request: redirect('/api/v1/', permanent=False)),
    path("api/v1/", include("publications.api")),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/ui/', SpectacularRedocView.as_view(url_name='optimap:schema'), name='redoc'),
    path("data/", data, name="data"),
    path('feed/rss', OptimetaFeed(), name="GeoRSSfeed"), 
    path("feed/atom", atomFeed(), name="GeoAtomfeed"),
    path("loginres/",loginres,name="loginres"),
    path("privacy/",privacypolicy,name="privacy"),
    path("loginconfirm/",Confirmationlogin,name="loginconfirm"),
    path("login/<str:token>", autheticate_via_magic_link, name="magic_link"),
    path("logout/", customlogout, name="logout"),
    path("usersettings/", user_settings, name="usersettings"),
    path("subscriptions/", user_subscriptions, name="subscriptions"),
    path("addsubscriptions/", add_subscriptions, name="addsubscriptions"),
    path("delete/", delete_account, name="delete"),
    path("changeuser/", change_useremail, name="changeuser"),
]
