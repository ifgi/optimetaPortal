from django.http.response import HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from publications.models import Publication
from django.core.cache import cache
from django.http.request import HttpRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from .forms import LoginForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.core.cache import cache
import secrets
import requests
from django.contrib import messages
from django.contrib.gis.geos import Polygon,MultiPolygon,GeometryCollection,Point,MultiPoint
from django.core import signing
from django.contrib.auth import login, get_user_model,logout
from django.views.decorators.http import require_GET
from django.contrib.auth.models import User
from django.core import signing
from django.urls import reverse
from urllib.parse import urlencode
from django.conf import settings
from bs4 import BeautifulSoup
import json
import os
import xml.dom.minidom
from xml.dom.minidom import parse


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

def EmailloginView(request):
          
    if request.method == "GET":
        form = LoginForm()
        
    else:
        form = LoginForm(request.POST)
        if form.is_valid():            
            email = form.cleaned_data["email"]
            subject = 'Test Email'
            data = {"email":email}
            link = signing.dumps(data)
            
            message =f"""\ Hello,You requested that we send you a link to log in to our app:    {link}   """
            try:
                send_mail(subject, message, from_email= settings.EMAIL_HOST_USER,recipient_list=[email])
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            return redirect("/success/")
    return render(request, "dashboard.html", {"form": form})

def successView(request):
    return HttpResponse("Success! We sent a log in link. Check your email.")

def optimap(request):
	return render(request,"main.html")
   

def loginres(request):
    
    email = request.POST.get('email', False)    
    subject = 'Test Email'
    data = {"email":email}
    token = secrets.token_urlsafe(nbytes=32)
    link = f"http://localhost:8000/{token}"
    cache.set(token, email, timeout=10 * 60)
    message =f"""Hello,You requested that we send you a link to log in to our app:    {link} .Please click on the link to login."""
    send_mail(subject, message, from_email= settings.EMAIL_HOST_USER,recipient_list=[email])
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
    user, _ = User.objects.get_or_create(username = email,email=email)
    login(request, user,backend='django.contrib.auth.backends.ModelBackend')
    return render(request,"confirmation_login.html")

    
@login_required
def customlogout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return render(request,"logout.html")

def user_settings(request):
    return render(request,'user_settings.html')

def user_subscriptions(request):
    return render(request,'subscriptions.html')

def delete_account(request):
    email = request.user.email
    Current_user = User.objects.filter(email = email)
    Current_user.delete()
    messages.info(request, "Your account has been successfully deleted.")
    return render(request,'deleteaccount.html')

def change_useremail(request):
    email_new = request.POST.get('email_new', False)
    currentuser = request.user
    
    if email_new:
        currentuser.email = email_new
        currentuser.username = email_new
        currentuser.save()
        #send email
        subject = 'Change Email'    
        token = secrets.token_urlsafe(nbytes=32)
        link = f"http://localhost:8000/{token}"
        cache.set(token, email_new, timeout=10 * 60)
        message =f"""Hello,You requested to change your email address.we have sent you a link to confirm your new email :    {link} .Please click on the link to complete the process."""
        send_mail(subject, message, from_email= settings.EMAIL_HOST_USER,recipient_list=[email_new])
        logout(request)

    return  render(request,'changeuser.html')

def get_geom(url):
    soup = BeautifulSoup(open(url,encoding="utf8"), "html.parser") #local file
    for tag in soup.find_all("meta"):
        if tag.get("name", None) == "DC.SpatialCoverage":
            data = tag.get("content", None)
            json_object = json.loads(data)
            return json_object


def harvest_data(request):
    url1 = os.path.join(os.getcwd(),'harvesting\\journal_1\\oai_dc.xml')
    DOMTree = xml.dom.minidom.parse(url1) # parse xml as DOM
    collection = DOMTree.documentElement
    articles = collection.getElementsByTagName("record")                                            
    no_articles = len(articles)  # number of articles in journal
    for i in range(no_articles):
        records = collection.getElementsByTagName("record")[i]
        identifier = records.getElementsByTagName("identifier")
        identifier_value = identifier[0].firstChild.nodeValue
        #get geometry from html
        #identifier_url = os.path.join(os.getcwd(),'harvesting\\journal_1\\article_01.html')
        #geom = get_geom(identifier_url)
        #geom_data = geom["features"][0]["geometry"]
        #geom_data_string = json.dumps(geom_data)
        bounds=MultiPolygon([Polygon(((-117.869537353516, 33.5993881225586),(-117.869537353516, 33.7736549377441),(-117.678024291992, 33.7736549377441),(-117.678024291992, 33.5993881225586),(-117.869537353516, 33.5993881225586)))])           
        gc = GeometryCollection(Point(0, 0), MultiPoint(Point(0, 0), Point(1, 1)), bounds)
        title = records.getElementsByTagName("dc:title")
        title_value = title[0].firstChild.nodeValue
        journal = records.getElementsByTagName("dc:publisher")
        journal_value = journal[0].firstChild.nodeValue
        date = records.getElementsByTagName("dc:date")
        date_value = date[0].firstChild.nodeValue
        link = records.getElementsByTagName("dc:identifier")
        link_value = link[0].firstChild.nodeValue
        publication = Publication(id = i+2 ,title = title_value,publicationDate = date_value, url = link_value , geometry = gc)
        publication.save()
    
    return render(request,'subscriptions.html')