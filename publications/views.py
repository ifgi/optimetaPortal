from email import message
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from publications.models import Publication
from rest_framework import generics
from publications.serializers import PublicationSerializer
from django.core import serializers
from django.urls import reverse_lazy
from django.http.request import HttpRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_http_methods
from .forms import LoginForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.mail import send_mail, BadHeaderError
from django.core.cache import cache
import secrets
import requests
from django.contrib.gis import geos
from django.contrib.gis.geos import GEOSGeometry,Polygon,MultiPolygon
import base64
from django.core import signing
from django.contrib.auth import login, get_user_model
from django.views.decorators.http import require_GET
from django.utils import timezone
from django.contrib.auth.models import User
from django.core import signing
from django.urls import reverse
from urllib.parse import urlencode

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


#populate database from datacite
def get_info():
    url = "https://api.test.datacite.org/dois/10.5438/0012"  # test change for production
    response = requests.get(url)
    data = response.json()
    bounds=MultiPolygon([Polygon(((-117.869537353516, 33.5993881225586),(-117.869537353516, 33.7736549377441),(-117.678024291992, 33.7736549377441),(-117.678024291992, 33.5993881225586),(-117.869537353516, 33.5993881225586)))])   
    article_data = Publication(name = data['data']['attributes']['titles'][0]['title'], location = bounds)
    article_data.save()

class PublicationsLoginView(TemplateView):

    template_name = 'magic.html'
    User = get_user_model()
        
    def home(request):
        if request.POST:
            email = request.POST.get("email")

            # if the user exists, send them an email
            if user := User.objects.filter(username=email, is_active=True).first():
                token = signing.dumps({"email": email})
                qs = urlencode({"token": token})

                magic_link = request.build_absolute_uri(
                    location=reverse("auth-magic-link"),
                ) + f"?{qs}"

                # send email
                send_mail(
                    "Login link",
                    f'Click <a href="{magic_link}">here</a> to login',
                    'from@example.com',
                    [email],
                    fail_silently=True,
                )
            return redirect("/")
        return render(request, 'magic.html', {})

def EmailLoginView(request):
          
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():            
            email = form.cleaned_data["email"]
            subject = 'Test Email'
            data = {"email":email}
            link = signing.dumps(data)
            
            message =f"""\ Hello,You requested that we send you a link to log in to our app:    {link}   """
            try:
                send_mail(subject, message, from_email= "optimetatest@gmail.com",recipient_list=[email])
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            return redirect("/publications/success/")
        else:
            HttpResponseBadRequest('Invalid form')
    else:
        return HttpResponseBadRequest('Invalid HTTP method')

def successView(request):
    return HttpResponse("Success! We sent a log in link. Check your email.")