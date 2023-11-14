# Generated by Django 4.2.5 on 2023-11-13 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cycle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cycle_img', models.ImageField(blank=True, default=None, null=True, upload_to='images/')),
                ('owner_id', models.CharField(blank=True, max_length=60, null=True)),
                ('dop', models.DateTimeField()),
                ('model', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('lend_or_sell', models.CharField(max_length=50)),
            ],
        ),
    ]
