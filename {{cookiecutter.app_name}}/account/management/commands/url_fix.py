import os
import time

from django.core.management.base import BaseCommand
from pathlib import Path

from account.management.commands.basically import get_active_directories, get_files

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Command(BaseCommand):
    help = "create urls versioning for all apps if not exist url directory"

    def handle(self, *args, **options):
        apps = get_active_directories()
        for app in apps:
            if 'urls' not in get_files(app):
                # os.popen(f'''echo "from django.urls import path \nurlpatterns = [  ]" > {PROJECT_DIR}/{app}/urls.py ''')
                os.popen(f'''mkdir -p {PROJECT_DIR}/{app}/urls/v1/''')
                time.sleep(1)
                os.popen(f'''echo "from {app}.urls import *" > {PROJECT_DIR}/{app}/urls/v1/__init__.py''')
                os.popen(f'''echo "from .urls import *" > {PROJECT_DIR}/{app}/urls/__init__.py''')
                os.popen(f'''echo "from django.urls import path \nurlpatterns = [\n]" >  {PROJECT_DIR}/{app}/urls/v1/urls.py''')
                os.popen(f'''echo "from django.urls import path, include\napp_name = '{app}'\nurlpatterns = [\n\tpath('api/v1/', include('account.urls.v1.urls')),\n]\n" >  {PROJECT_DIR}/{app}/urls/urls.py''')
                os.popen(f'touch {PROJECT_DIR}/{app}/urls/v1/views.py')
                os.popen(f'''echo "from rest_framework import serializers\n#create your serializers" > {PROJECT_DIR}/{app}/urls/v1/serializers.py''')
        # for app in apps:

        # dirs = os.popen(f"ls -d */").read()
        # dirs = [dir.replace("/","") for dir in dirs.split("\n") if dir]
        # for dir in dirs:
        #     files = os.popen(f"ls {PROJECT_DIR}/{dir}").read()
        #     files = [file for file in files.split("\n") if files]
        #     if 'models' in files:

        # print(subprocess.run(["ls", f"{PROJECT_DIR}"]))
        # self.stdout.write(f"My custom command executed successfully {BASE_DIR}")
