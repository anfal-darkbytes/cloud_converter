import os
from django.apps import AppConfig
from .thread import CleanUpFiles


class CloudconverterappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cloudConverterApp'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':
            cleanup_thread = CleanUpFiles()
            cleanup_thread.daemon = True
            cleanup_thread.start()
