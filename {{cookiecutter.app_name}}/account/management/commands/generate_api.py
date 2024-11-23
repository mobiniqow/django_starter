import os
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps


class Command(BaseCommand):
    help = 'Generates serializers, viewsets, and URLs for all models in a specified app.'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='Name of the Django app for which to generate API files.')

    def handle(self, *args, **options):
        app_name = options['app_name']

        # پیدا کردن اپلیکیشن
        try:
            app_config = apps.get_app_config(app_name)
        except LookupError:
            raise CommandError(f"App '{app_name}' does not exist.")

        # مسیرها
        app_path = app_config.path
        api_dir = os.path.join(app_path, "urls/v1")
        serializers_path = os.path.join(api_dir, "serializers.py")
        views_path = os.path.join(api_dir, "views.py")
        urls_path = os.path.join(api_dir, "urls.py")

        # ایجاد دایرکتوری urls/v1
        os.makedirs(api_dir, exist_ok=True)

        serializers_content = ["from rest_framework import serializers"]
        views_content = [
            "from rest_framework import viewsets",
            "from rest_framework.permissions import IsAuthenticated",
            "from .serializers import *",
        ]
        urls_content = [
            "from rest_framework.routers import DefaultRouter",
            f"from {app_name}.urls.v1.views import *",  # اضافه کردن ایمپورت views
            ""
        ]
        router_lines = ["router = DefaultRouter()"]

        # ایمپورت مدل‌ها
        model_imports = []
        for model in app_config.get_models():
            model_name = model.__name__
            model_imports.append(f"from {app_name}.models import {model_name}")

        serializers_content.extend(model_imports)
        views_content.extend(model_imports)

        # پردازش هر مدل
        for model in app_config.get_models():
            model_name = model.__name__
            model_lower = model_name.lower()

            # بررسی وجود فیلد user
            has_user_fk = any(
                field.name == "user" and field.related_model and field.related_model._meta.model_name == "user"
                for field in model._meta.get_fields()
            )

            # افزودن Serializer
            serializers_content.append(f"\n\nclass {model_name}Serializer(serializers.ModelSerializer):")
            serializers_content.append(f"    class Meta:")
            serializers_content.append(f"        model = {model_name}")
            serializers_content.append(f"        fields = '__all__'")

            # افزودن ViewSet
            views_content.append(f"\n\nclass {model_name}ViewSet(viewsets.ModelViewSet):")
            views_content.append(f"    permission_classes = [IsAuthenticated]")
            views_content.append(f"    serializer_class = {model_name}Serializer")

            if has_user_fk:
                views_content.append(f"    def get_queryset(self):")
                views_content.append(f"        return {model_name}.objects.filter(user=self.request.user)")
            else:
                views_content.append(f"    def get_queryset(self):")
                views_content.append(f"        return {model_name}.objects.all()")
                views_content.append(f"\n    def has_permission(self, request, view):")
                views_content.append(f"        if request.method in ['GET']: return True")
                views_content.append(f"        return False")

            # افزودن به Router
            router_lines.append(f"router.register(r'{model_lower}', {model_name}ViewSet)")

        # تکمیل محتوای URLs
        urls_content.extend(router_lines)
        urls_content.append("")
        urls_content.append("urlpatterns = router.urls")

        # نوشتن فایل‌ها
        try:
            with open(serializers_path, "w") as f:
                f.write("\n".join(serializers_content))
            self.stdout.write(self.style.SUCCESS(f"Serializers written to {serializers_path}"))

            with open(views_path, "w") as f:
                f.write("\n".join(views_content))
            self.stdout.write(self.style.SUCCESS(f"ViewSets written to {views_path}"))

            with open(urls_path, "w") as f:
                f.write("\n".join(urls_content))
            self.stdout.write(self.style.SUCCESS(f"URLs written to {urls_path}"))
        except Exception as e:
            raise CommandError(f"An error occurred while writing files: {e}")

        self.stdout.write(self.style.SUCCESS(f"API generation for app '{app_name}' completed successfully!"))
