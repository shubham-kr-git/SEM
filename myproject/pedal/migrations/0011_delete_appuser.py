# Generated by Django 4.2.5 on 2023-11-13 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedal', '0010_appuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AppUser',
        ),
    ]