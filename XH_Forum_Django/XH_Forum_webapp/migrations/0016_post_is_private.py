# Generated by Django 3.2.24 on 2024-05-15 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('XH_Forum_webapp', '0015_auto_20240515_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]
