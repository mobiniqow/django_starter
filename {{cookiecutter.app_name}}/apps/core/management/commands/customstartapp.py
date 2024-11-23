import os
import sys
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creates a new app with custom folder structure including service layer'

    def add_arguments(self, parser):
        # دریافت نام اپ از ورودی
        parser.add_argument('app_name', type=str, help='The name of the app to be created')

    def handle(self, *args, **options):
        app_name = options['app_name']
        self.stdout.write(f'Creating app: {app_name}')

        # مسیر پوشه اپ جدید
        app_path = os.path.join('apps', app_name)

        # بررسی وجود پوشه
        if os.path.exists(app_path):
            self.stdout.write(self.style.ERROR(f"App '{app_name}' already exists!"))
            return

        # ایجاد پوشه‌های اصلی
        os.makedirs(app_path, exist_ok=True)

        # ایجاد پوشه‌های داخلی: public, admin, user, services
        os.makedirs(os.path.join(app_path, 'public'), exist_ok=True)
        os.makedirs(os.path.join(app_path, 'admin'), exist_ok=True)
        os.makedirs(os.path.join(app_path, 'user'), exist_ok=True)
        os.makedirs(os.path.join(app_path, 'services'), exist_ok=True)

        # ایجاد فایل‌های اصلی
        self.create_file(os.path.join(app_path, '__init__.py'), f'# {app_name} app')
        self.create_file(os.path.join(app_path, 'models.py'), f'# Models for {app_name}')
        self.create_file(os.path.join(app_path, 'urls.py'), self.get_app_urls())

        # ایجاد فایل‌های urls و views برای هر بخش (public, admin, user)
        self.create_section_files(app_name, 'public')
        self.create_section_files(app_name, 'admin')
        self.create_section_files(app_name, 'user')

        # ایجاد سرویس‌ها برای اپ
        self.create_service_files(app_name)

        self.stdout.write(self.style.SUCCESS(f"App '{app_name}' created successfully!"))

    def create_file(self, file_path, content):
        with open(file_path, 'w') as f:
            f.write(content)

    def get_app_urls(self):
        return """from django.urls import path, include
from .public import urls as public_urls
from .admin import urls as admin_urls
from .user import urls as user_urls

urlpatterns = [
    path('public/', include(public_urls)),
    path('admin/', include(admin_urls)),
    path('user/', include(user_urls)),
]"""

    def create_section_files(self, app_name, section):
        # مسیر پوشه هر بخش (public, admin, user)
        section_path = os.path.join('apps', app_name, section)

        # ایجاد فایل urls برای هر بخش
        self.create_file(os.path.join(section_path, 'urls.py'), self.get_section_urls(section))

        # ایجاد فایل views برای هر بخش
        self.create_file(os.path.join(section_path, 'views.py'), self.get_section_views(section))

        # ایجاد فایل tests برای هر بخش
        self.create_file(os.path.join(section_path, 'tests.py'), self.get_section_tests(section))

    def get_section_urls(self, section):
        return f"""from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.list_view, name='{section}_list'),
]"""

    def get_section_views(self, section):
        return f"""from django.shortcuts import render
from django.http import JsonResponse
from apps.{section}.services import {section.capitalize()}Service

def list_view(request):
    service = {section.capitalize()}Service()
    data = service.get_list()
    return JsonResponse(data)"""

    def get_section_tests(self, section):
        return f"""from django.test import TestCase

class {section.capitalize()}TestCase(TestCase):
    def test_example(self):
        response = self.client.get('/{section}/list/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json())"""

    def create_service_files(self, app_name):
        # مسیر پوشه سرویس
        service_path = os.path.join('apps', app_name, 'services')

        # ایجاد فایل سرویس
        service_content = """class {service_name}Service:
    def get_list(self):
        return {'message': 'List from {service_name} service'}
"""
        self.create_file(os.path.join(service_path, f'{app_name.lower()}_service.py'), service_content.format(service_name=app_name))

