import json
from kafka import KafkaProducer
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from myapp.models import MyModel  # این را با مدل‌های خودتان جایگزین کنید

# Kafka Producer برای ارسال داده‌ها
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],  # آدرس Kafka Broker
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

class CDCMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # انجام کارهای معمولی میدلور
        response = self.get_response(request)
        return response

# سیگنال‌ها برای ارسال تغییرات به Kafka
@receiver(post_save, sender=MyModel)
def model_post_save(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    data = {
        'action': action,
        'model': sender.__name__,
        'data': instance_to_dict(instance)  # تابعی برای تبدیل داده به دیکشنری
    }
    producer.send('cdc-topic', value=data)
    producer.flush()

@receiver(post_delete, sender=MyModel)
def model_post_delete(sender, instance, **kwargs):
    data = {
        'action': 'deleted',
        'model': sender.__name__,
        'data': instance_to_dict(instance)
    }
    producer.send('cdc-topic', value=data)
    producer.flush()

def instance_to_dict(instance):
    """
    تبدیل مدل به دیکشنری. شما باید این تابع را برای هر مدل خاص خود
    تنظیم کنید.
    """
    return {field.name: getattr(instance, field.name) for field in instance._meta.fields}
