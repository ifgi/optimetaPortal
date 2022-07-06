from django.shortcuts import render
from django.views.generic.base import TemplateView
from publications.models import Publication
from rest_framework import generics
from publications.serializers import PublicationSerializer
from django.core import serializers
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.http.request import HttpRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_http_methods
from .forms import MagicLinkForm
from django.core.mail import send_mail
from django.core.cache import cache
import secrets
import requests
from django.contrib.gis import geos
from django.contrib.gis.geos import GEOSGeometry,Polygon,MultiPolygon

class PublicationsMapView(TemplateView):
    """publications map view."""

    template_name = "map.html"

#class MarkerCreate(generics.RetrieveAPIView):
    # API endpoint that allows return of muiltipolygon
    #queryset = serializers.serialize("json", Marker.objects.all()),
    #serializer_class = publicationserializer


'''class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact:success')

    def form_valid(self, form):
        # Calls the custom send method
        form.send()
        return super().form_valid(form)

class ContactSuccessView(TemplateView):
    template_name = 'success.html'''

@require_http_methods(["GET", "POST"])
def home(request: HttpRequest):
    if request.POST:
        form = MagicLinkForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            token = secrets.token_urlsafe(nbytes=32)
            link = f"http://localhost:8000/magic-link/{token}"
            cache.set(token, email, timeout=10 * 60)
            send_mail(
                subject="Magic Link",
                message=f"You link: {link}",
                from_email="amal@amalshaji.com",
                recipient_list=[email],
                fail_silently=True,
            )
    return render(request, "magic.html")
    

@require_GET
@login_required
def dashboard(request: HttpRequest):
    return render(request, "dashboard.html")

#populate database from datacite
def get_info():
    url = "https://api.test.datacite.org/dois/10.5438/0012"  # test change for production
    response = requests.get(url)
    data = response.json()
    bounds=MultiPolygon([Polygon(((-117.869537353516, 33.5993881225586),(-117.869537353516, 33.7736549377441),(-117.678024291992, 33.7736549377441),(-117.678024291992, 33.5993881225586),(-117.869537353516, 33.5993881225586)))])   
    article_data = Publication(name = data['data']['attributes']['titles'][0]['title'], location = bounds)
    article_data.save()
    

    