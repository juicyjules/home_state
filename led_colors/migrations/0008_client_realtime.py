# Generated by Django 3.1.7 on 2021-03-13 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('led_colors', '0007_client_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='realtime',
            field=models.BooleanField(default=False),
        ),
    ]
