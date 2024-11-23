from django.db import models
from django.utils import timezone
import uuid


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
