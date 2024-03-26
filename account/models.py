import re
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_jalali.db import models as jmodels
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


def phone_validator(v):
    pattern = r"^09[0|1|2|3][0-9]{8}$"
    if not re.match(pattern, v):
        raise ValidationError("invalid phone number")


class BasicUserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        if not phone:
            raise ValueError("Users must enter a phone")

        user = self.model(phone=phone)
        user.state = User.State.SUSPEND
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password=None):
        user = self.model(phone=phone)
        user.is_staff = True
        user.set_password(password)
        user.state = User.State.ACTIVE
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    class State(models.IntegerChoices):
        SUSPEND = 0
        ACTIVE = 1
        REPORTED = 2
        BANNED = 3

    created_at = jmodels.jDateField(auto_now_add=True)
    updated_at = jmodels.jDateField(auto_now=True)
    avatar = models.FileField(upload_to='account/user/avatar',
                              validators=[FileExtensionValidator(['jpg', 'png', 'jpeg']), ], blank=True)
    state = models.IntegerField(choices=State.choices, default=State.SUSPEND)
    user_name = models.CharField(max_length=33)
    phone = models.CharField(max_length=17, unique=True, validators=[phone_validator])
    objects = BasicUserManager()
    USERNAME_FIELD = "phone"
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.phone

    @property
    def is_active(self):
        return self.state == User.State.ACTIVE

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff


