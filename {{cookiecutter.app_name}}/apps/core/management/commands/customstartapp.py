import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creates a new app with custom folder structure including service layer, versioning, CQRS (Command Query Responsibility Segregation), and more'

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
        os.makedirs(os.path.join(app_path, 'services', 'command'), exist_ok=True)
        os.makedirs(os.path.join(app_path, 'services', 'query'), exist_ok=True)

        # ایجاد فایل‌های اصلی
        self.create_file(os.path.join(app_path, '__init__.py'), f'# {app_name} app')
        self.create_file(os.path.join(app_path, 'models.py'), f'# Models for {app_name}')
        self.create_file(os.path.join(app_path, 'urls.py'), self.get_app_urls())

        # ایجاد فایل‌های urls و views برای هر بخش (public, admin, user)
        self.create_section_files(app_name, 'public', version='v1')
        self.create_section_files(app_name, 'admin', version='v1')
        self.create_section_files(app_name, 'user', version='v1')

        # ایجاد سرویس‌ها برای اپ
        self.create_service_files(app_name)

        # ایجاد تست‌ها
        self.create_test_files(app_name)

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

    def create_section_files(self, app_name, section, version='v1'):
        # مسیر پوشه هر بخش (public, admin, user)
        section_path = os.path.join('apps', app_name, section)

        # ایجاد پوشه برای نسخه
        versioned_path = os.path.join(section_path, version)
        os.makedirs(versioned_path, exist_ok=True)

        # ایجاد فایل‌های urls، views و tests برای هر بخش با ورژن
        self.create_file(os.path.join(versioned_path, 'urls.py'), self.get_section_urls(section, version))
        self.create_file(os.path.join(versioned_path, 'views.py'), self.get_section_views(section, version))
        self.create_file(os.path.join(versioned_path, 'tests.py'), self.get_section_tests(section, version))

    def get_section_urls(self, section, version):
        return f"""from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.list_view, name='{section}_{version}_list'),
]"""

    def get_section_views(self, section, version):
        return f"""from django.shortcuts import render
from django.http import JsonResponse
from apps.{section}.services.query import {section.capitalize()}QueryService
from apps.{section}.services.command import {section.capitalize()}CommandService

def list_view(request):
    query_service = {section.capitalize()}QueryService()
    data = query_service.get_list()
    return JsonResponse(data)"""

    def get_section_tests(self, section, version):
        return f"""from django.test import TestCase

class {section.capitalize()}TestCase(TestCase):
    def test_example(self):
        response = self.client.get('/{section}/{version}/list/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json())"""

    def create_service_files(self, app_name):
        # مسیر پوشه سرویس
        service_path = os.path.join('apps', app_name, 'services')

        # ایجاد سرویس‌های Command و Query برای هر بخش
        for section in ['public', 'admin', 'user']:
            # Command Service
            command_service_content = """class {service_name}CommandService:
    def create(self, data):
        # عملیات ایجاد
        return {'message': 'Created successfully'}
"""
            self.create_file(os.path.join(service_path, 'command', f'{section.capitalize()}CommandService.py'),
                             command_service_content.format(service_name=section.capitalize()))

            # Query Service
            query_service_content = """class {service_name}QueryService:
    def get_list(self):
        # عملیات خواندن لیست
        return {'message': 'List from {service_name} query service'}
"""
            self.create_file(os.path.join(service_path, 'query', f'{section.capitalize()}QueryService.py'),
                             query_service_content.format(service_name=section.capitalize()))

    def create_test_files(self, app_name):
        # مسیر پوشه تست‌ها
        test_path = os.path.join('apps', app_name, 'tests')

        # ایجاد فایل تست‌ها
        test_content = """from django.test import TestCase

class BasicTestCase(TestCase):
    def test_example(self):
        response = self.client.get('/public/v1/list/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json())
"""
        self.create_file(os.path.join(test_path, 'test_basic.py'), test_content)
