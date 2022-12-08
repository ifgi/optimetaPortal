from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.core.cache import cache
from django.http.request import HttpRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from .forms import LoginForm
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.core.cache import cache
import secrets
from django.contrib import messages
from django.core import signing
from django.contrib.auth import login, get_user_model,logout
from django.views.decorators.http import require_GET
from django.contrib.auth.models import User
from django.core import signing
from django.urls import reverse
from urllib.parse import urlencode
from django.conf import settings


#populate database from datacite

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
    if 'logged_in' in request.COOKIES and 'username' in request.COOKIES:
        context = {
                'useremail':request.COOKIES['useremail'],
                'login_status':request.COOKIES.get('logged_in_status'),
            }
        response = render(request,"main.html",context)
    else:
        response = render(request,"main.html")
    
    return response

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
        response = render(request, "error.html", {
            'error': {
                'class': 'danger',
                'title': 'Authentication failed!',
                'text': 'Magic Link invalid/expired.'
            }
        })
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
    eemail = request.user.email
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