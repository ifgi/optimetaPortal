from django.core.mail import send_mail
from django.core import signing
data = {"email": "to@yourbestuser.com"}
value = signing.dumps(data)
print (value)

send_mail(
    'That’s your subject',
    'That’s your message body:' + value,
    'from@yourdjangoapp.com',
    ['to@yourbestuser.com'],
    fail_silently=False,
)

send_mail(
    subject = 'Test Email',
    message = 'Hi, David.Sending you a test email.See you @2',
    from_email = 'optimetatest@gmail.com' ,
    recipient_list = ['daniel.nuest@gmail.com'],
    fail_silently = False,
)