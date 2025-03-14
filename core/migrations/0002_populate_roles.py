# Generated by Django 5.1.7 on 2025-03-12 21:42

from django.db import migrations


def insert_roles(apps, schema_editor):
    Role = apps.get_model('core', 'Role')
    Role.objects.bulk_create([
        Role(title="General Manager", rank=1),
        Role(title="Director", rank=2),
        Role(title="Team Leader", rank=3),
        Role(title="Programmer", rank=4),
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_roles),
    ]
