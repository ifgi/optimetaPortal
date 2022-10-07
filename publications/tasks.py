from django_q.models import Schedule
Schedule.objects.create(
    func='publications.views.get_info',
    schedule_type=Schedule.DAILY
)

