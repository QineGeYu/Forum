# Generated by Django 3.2.24 on 2024-04-28 11:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('XH_Forum_webapp', '0009_auto_20240428_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='contacted_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
    ]
