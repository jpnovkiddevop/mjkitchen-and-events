# Generated by Django 4.2.7 on 2023-11-16 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='Venue',
            new_name='venue',
        ),
    ]
