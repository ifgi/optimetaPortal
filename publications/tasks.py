from django_q.models import Schedule
from datetime import date, timezone
from publications.models import Publication
from django.core.mail import send_mail

Schedule.objects.create(
    func='publications.views.get_info',
    schedule_type=Schedule.DAILY
)

def new_manuscript_updates():
    """
    send email for manuscript updates
    """
    one_minute_ago = timezone.now() - timezone.timedelta(minutes=1)
    new_manuscripts = Publication.objects.filter(
        date = one_minute_ago
    )
    subject = 'New Manuscripts'
    email = "test@example.com"
    message =f"""\ Hello, we send you updated manuscripts that you were looking for:    {new_manuscripts}   """
    send_mail(subject, message, from_email= "optimetageo@gmail.com",recipient_list=[email])

Schedule.objects.create(
    func='publications.tasks.new_manuscript_updates',
    schedule_type=Schedule.MONTHLY
)
