# Generated by Django 2.1.7 on 2019-05-14 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='root',
        ),
    ]
