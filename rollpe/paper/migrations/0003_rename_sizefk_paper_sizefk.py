# Generated by Django 5.1.4 on 2025-01-24 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paper', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paper',
            old_name='sizeFk',
            new_name='sizeFK',
        ),
    ]
