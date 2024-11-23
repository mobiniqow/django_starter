import os
from django.db import models
from django.utils import timezone
import uuid
import json
from kafka import KafkaProducer
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Kafka Producer برای ارسال تغییرات
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],  # آدرس Kafka Broker
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Deleted At")

    class Meta:
        abstract = True
        ordering = ['-created_at']  # به‌طور پیش‌فرض نتایج جدیدتر اول نمایش داده شوند

    def delete(self, using=None, keep_parents=False):
        """
        پیاده‌سازی حذف نرم. به‌جای حذف فیزیکی رکورد، تاریخ حذف را تنظیم می‌کند.
        """
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save()

    def restore(self):
        """
        برای بازگرداندن رکورد حذف شده نرم.
        """
        self.deleted_at = None
        self.is_active = True
        self.save()

    def soft_deleted(self):
        """
        برای فیلتر کردن رکوردهای حذف شده نرم.
        """
        return self.deleted_at is not None

    @classmethod
    def active_objects(cls):
        """
        برای دریافت رکوردهای فعال که حذف نشده‌اند.
        """
        return cls.objects.filter(is_active=True, deleted_at__isnull=True)

    @classmethod
    def all_inclusive(cls):
        """
        دریافت تمامی رکوردها، حتی حذف‌شده‌ها.
        """
        return cls.objects.all()

    def send_to_cdc(self, action, section="command"):
        """
        ارسال تغییرات به Kafka یا سیستم مشابه.
        این متد برای عملیات‌های Command استفاده می‌شود.
        """
        data = {
            'action': action,
            'model': self.__class__.__name__,
            'data': self.to_dict(),
            'section': section  # برای شناسایی نوع عملیات (Command یا Query)
        }
        producer.send('cdc-topic', value=data)
        producer.flush()

    def to_dict(self):
        """
        تبدیل مدل به دیکشنری برای ارسال به Kafka یا دیگر سیستم‌ها.
        """
        return {field.name: getattr(self, field.name) for field in self._meta.fields}

# سیگنال‌ها برای ارسال تغییرات به Kafka
@receiver(post_save)
def model_post_save(sender, instance, created, **kwargs):
    # فقط برای عملیات‌های Command (ایجاد و بروزرسانی)
    if hasattr(instance, 'send_to_cdc'):
        action = "created" if created else "updated"
        instance.send_to_cdc(action)

@receiver(post_delete)
def model_post_delete(sender, instance, **kwargs):
    # فقط برای عملیات‌های Command (حذف)
    if hasattr(instance, 'send_to_cdc'):
        instance.send_to_cdc("deleted")
