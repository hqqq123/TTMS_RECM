# Generated by Django 2.1.7 on 2019-05-08 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seat', '0004_seat_selected'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seat',
            name='selected',
        ),
    ]
