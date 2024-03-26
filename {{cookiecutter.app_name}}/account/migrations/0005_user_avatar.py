# Generated by Django 4.1.1 on 2022-12-10 21:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0004_user_groups_user_is_superuser_user_user_permissions"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="avatar",
            field=models.FileField(
                blank=True,
                upload_to="account/user/avatar",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        ["jpg", "png", "jpeg"]
                    )
                ],
            ),
        ),
    ]