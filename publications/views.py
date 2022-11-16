from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from publications.models import Publication
from .forms import LoginForm
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
import requests
from django.contrib.gis.geos import Polygon,MultiPolygon
from django.core import signing
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core import signing
from django.urls import reverse
from urllib.parse import urlencode
from django.core.cache import cache
import secrets
from django.core.cache.backends import locmem
from django.http.response import HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth import login


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
    article_data = Publication(title = data['data']['attributes']['titles'][0]['title'], geometry = bounds)
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

def successView(request):
    return HttpResponse("Success! We sent a log in link. Check your email.")

def optimap(request):
    return render(request, 'main.html')

def loginres(request):
    
    email = request.POST.get('email', False)
    subject = 'Test Email'
    data = {"email":email}
    token = secrets.token_urlsafe(nbytes=32)
    link = f"http://localhost:8000/{token}"
    cache.set(token, email, timeout=10 * 60)
    message =f"""Hello,You requested that we send you a link to log in to our app:    {link} .Please click on the link to login."""
    send_mail(subject, message, from_email= "optimetageo@gmail.com",recipient_list=[email])
    #return HttpResponse("Success! We sent a log in link. Check your email.")
    return render(request,'login_response.html')

def privacypolicy(request):
    return render(request,'privacy.html')
	
def Confirmationlogin(request):
    return render(request,'confirmation_login.html')
	
@require_GET
def autheticate_via_magic_link(request: HttpRequest, token: str):
    email = cache.get(token)    
    if email is None:
        return HttpResponseBadRequest(content="Magic Link invalid/expired")
    cache.delete(token)
    user, _ = User.objects.get_or_create(email=email)
    login(request, user,backend='django.core.cache.backends.locmem.LocMemCache')
    return render(request,"confirmation_login.html")