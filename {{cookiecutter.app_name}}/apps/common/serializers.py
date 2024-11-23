from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    """
    Base Serializer that provides common functionality for all serializers.
    """
    # افزودن فیلدهای مشترک، مثلا برای زمانی که می‌خواهید تاریخ ایجاد یا وضعیت فعال بودن را بازنمایی کنید
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(default=True, read_only=True)

    class Meta:
        abstract = True  # این مدل سریالایزر به‌طور مستقیم استفاده نمی‌شود

    def to_representation(self, instance):
        """
        Override the to_representation method to add custom transformations.
        """
        representation = super().to_representation(instance)

        # مثلا می‌توانید فیلدهای اضافی را برای بهبود پاسخ API اضافه کنید
        representation['status'] = 'active' if instance.is_active else 'inactive'

        return representation

    def create(self, validated_data):
        """
        Override the create method to add common logic.
        """
        # برای ایجاد رکورد از داده‌های معتبر استفاده می‌کنیم
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Override the update method to add common logic.
        """
        # برای بروزرسانی رکورد از داده‌های معتبر استفاده می‌کنیم
        return super().update(instance, validated_data)

    def validate(self, data):
        """
        Override the validate method to add custom validation logic.
        """
        # می‌توانید اعتبارسنجی‌های عمومی مثل بررسی وضعیت فعال بودن را انجام دهید
        if not data.get('is_active'):
            raise serializers.ValidationError('The record must be active.')
        return data
