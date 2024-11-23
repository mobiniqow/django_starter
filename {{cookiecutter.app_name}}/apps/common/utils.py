import os
import time
import random
import string
import re
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.response import Response
from django.utils.translation import get_language_from_request


# ================================
# 1. مدیریت تاریخ و زمان
# ================================

def get_current_timestamp():
    """
    دریافت timestamp کنونی
    """
    return int(time.time())


def format_date(date_obj, date_format='%Y-%m-%d'):
    """
    تبدیل شیء تاریخ به فرمت دلخواه
    """
    if not date_obj:
        return None
    return date_obj.strftime(date_format)


def get_time_difference_in_days(start_date, end_date):
    """
    محاسبه تفاوت زمانی بین دو تاریخ به صورت تعداد روز
    """
    delta = end_date - start_date
    return delta.days


# ================================
# 2. مدیریت رشته‌ها
# ================================

def is_valid_email(email):
    """
    اعتبارسنجی ایمیل با استفاده از الگوی regular expression
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(email_regex, email))


def slugify_string(input_string):
    """
    تبدیل رشته به فرمت slug مناسب برای URL
    """
    slug = re.sub(r'[\W_]+', '-', input_string.lower())
    return slug


# ================================
# 3. مدیریت فایل‌ها
# ================================

def get_file_extension(filename):
    """
    دریافت پسوند فایل از نام فایل
    """
    return os.path.splitext(filename)[1]


def save_file(file, directory='uploads/'):
    """
    ذخیره فایل در دایرکتوری مشخص‌شده
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return file_path


# ================================
# 4. مدیریت داده‌ها و پایگاه داده
# ================================

def get_object_or_404_custom(model_class, **kwargs):
    """
    دریافت شیء از مدل با شرایط خاص، در صورت عدم وجود آن، خطا می‌دهد
    """
    try:
        return model_class.objects.get(**kwargs)
    except model_class.DoesNotExist:
        raise Http404(f"{model_class.__name__} not found with the given conditions.")


def bulk_create_with_default(model_class, data, default_values=None):
    """
    وارد کردن دسته‌ای داده‌ها به پایگاه داده با مقادیر پیش‌فرض
    """
    if default_values:
        for obj in data:
            for field, value in default_values.items():
                if field not in obj:
                    obj[field] = value
    model_class.objects.bulk_create([model_class(**obj) for obj in data])


# ================================
# 5. توابع کمکی برای عملیات‌های خاص
# ================================

def generate_random_string(length=8):
    """
    ایجاد یک رشته تصادفی از حروف و اعداد
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def calculate_age(birthdate):
    """
    محاسبه سن فرد با توجه به تاریخ تولد
    """
    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


# ================================
# 6. مدیریت ورودی‌ها و پاسخ‌ها
# ================================

def response_with_status(status_code, message, data=None):
    """
    بازگشت پاسخ با کد وضعیت، پیام و داده‌ها
    """
    response = {
        'status_code': status_code,
        'message': message,
        'data': data if data else {},
    }
    return Response(response, status=status_code)


# ================================
# 7. مدیریت امنیت و اعتبارسنجی
# ================================

def hash_password(password):
    """
    هش کردن رمز عبور برای ذخیره در پایگاه داده
    """
    return make_password(password)


def check_password_hash(password, hashed_password):
    """
    بررسی صحیح بودن رمز عبور
    """
    return check_password(password, hashed_password)


# ================================
# 8. توابع کمکی برای درخواست‌ها و API
# ================================

def get_client_ip(request):
    """
    دریافت IP واقعی کاربر از درخواست
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_language_from_request(request):
    """
    دریافت زبان انتخاب‌شده از درخواست
    """
    return get_language_from_request(request)
ظ