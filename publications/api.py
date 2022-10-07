"""Markers API URL Configuration."""

from rest_framework import routers

from publications.viewsets import PublicationViewSet

router = routers.DefaultRouter()
router.register(r"publications", PublicationViewSet)

urlpatterns = router.urls
