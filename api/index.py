import os

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "padel_prj.settings")

app = get_wsgi_application()

if os.environ.get("RUN_MIGRATIONS_ON_STARTUP", "1") == "1":
    call_command("migrate", interactive=False, verbosity=0)

if os.environ.get("BOOTSTRAP_ADMIN", "1") == "1":
    call_command("bootstrap_admin", verbosity=0)
