import os
from pathlib import Path
import environ
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '../ecommerce/../../.env'))
class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username=env("ADMIN_NAME"),
                password=env("ADMIN_PASSWORD")
            )
        print('Superuser has been created.')