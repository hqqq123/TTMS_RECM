# Generated by Django 2.1.7 on 2019-05-07 00:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seat', '0002_auto_20190506_1008'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seat',
            old_name='studio_id',
            new_name='studio',
        ),
    ]