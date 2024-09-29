from django.apps import AppConfig
import os

class SpinningGameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'spinning_game'

    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true':
            from . import auto_spin