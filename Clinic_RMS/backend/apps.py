from unicodedata import name
from django.apps import AppConfig


class BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend'

    # Configure the signals of the app
    def ready(self):
        import backend.signals