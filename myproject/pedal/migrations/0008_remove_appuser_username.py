# Generated by Django 4.2.5 on 2023-11-13 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedal', '0007_appuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appuser',
            name='username',
        ),
    ]
