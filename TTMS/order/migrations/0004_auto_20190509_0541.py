# Generated by Django 2.1.7 on 2019-05-09 05:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20190509_0538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
