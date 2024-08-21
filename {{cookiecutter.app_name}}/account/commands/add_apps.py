import os
import time

from django.core.management.base import BaseCommand
from pathlib import Path
from core.settings.base import INSTALLED_APPS
from account.management.commands.basically import get_active_directories, get_files
import os
PROJECT_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Command(BaseCommand):
    help = "add apps to urls"

    def handle(self, *args, **options):
        new_install_apps = []
        apps = get_active_directories()
        for i in apps:
            if i not in INSTALLED_APPS and f'{i}.apps.{i.title()}Config' not in INSTALLED_APPS:
                new_install_apps.append(f'{i}.apps.{i.title()}Config')
        settings = os.popen(f'less {PROJECT_DIR}/core/settings/base.py').readlines()
        os.popen(f'rm {PROJECT_DIR}/core/settings/base.py')
        time.sleep(1)
        with open(f'{PROJECT_DIR}/core/settings/base.py', 'w+') as f:
            for i in settings:
                f.writelines(i)
                # print(i.strip())
                print(i.strip())
                print("django.contrib.staticfiles")
                if i.strip() == '"django.contrib.staticfiles",':
                    for j in new_install_apps:
                        f.writelines(f'    "{j}",\n')
