# Generated by Django 2.2.6 on 2019-11-22 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phenopackets', '0009_auto_20191122_2040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metadata',
            name='resources',
        ),
    ]