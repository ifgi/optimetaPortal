from django.apps import AppConfig


class PublicationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'publications'

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from . import signals
