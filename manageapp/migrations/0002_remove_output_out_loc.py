# Generated by Django 2.1.5 on 2020-09-21 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manageapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='output',
            name='out_loc',
        ),
    ]