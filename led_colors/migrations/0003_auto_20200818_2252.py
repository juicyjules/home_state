# Generated by Django 3.0.9 on 2020-08-18 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('led_colors', '0002_auto_20200818_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='last_connection',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='ip',
            field=models.BinaryField(default=b'', max_length=4),
        ),
    ]
