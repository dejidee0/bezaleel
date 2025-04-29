from django.apps import AppConfig
from django.core.management import call_command

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # def ready(self):
        # Trigger the superuser creation command
        # call_command('create_superuser')
