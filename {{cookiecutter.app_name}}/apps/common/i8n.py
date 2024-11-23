# django-admin makemessages -l fa  # برای زبان فارسی
# django-admin compilemessages
import os
LANGUAGES = [
    ('en', 'English'),
    ('fa', 'فارسی'),
    ('de', 'Deutsch'),
    ('fr', 'Français'),
    # زبان‌های دیگر که می‌خواهید اضافه کنید
]

# زبان پیش‌فرض سایت
LANGUAGE_CODE = 'en'
USE_I18N = True        # فعال کردن i18n
USE_L10N = True        # فعال کردن l10n
# مسیری که فایل‌های ترجمه در آن ذخیره می‌شود
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),  # مسیر پوشه locale که فایل‌های ترجمه در آن ذخیره می‌شوند
]
# urlpatterns = [
#     path('i18n/', include('django.conf.urls.i18n')),  # مسیر تغییر زبان
#     # سایر مسیرها
# ]