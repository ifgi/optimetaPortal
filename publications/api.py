"""Markers API URL Configuration."""

from rest_framework import routers

from publications.viewsets import PublicationViewSet,SubscriptionViewset

router = routers.DefaultRouter()
router.register(r"publications", PublicationViewSet)
router.register(r"subscriptions",SubscriptionViewset)
urlpatterns = router.urls
