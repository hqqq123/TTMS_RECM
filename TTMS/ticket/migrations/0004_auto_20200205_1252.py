# Generated by Django 2.1.7 on 2020-02-05 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0003_auto_20190516_1340'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='order',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='schedule',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='seat',
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]