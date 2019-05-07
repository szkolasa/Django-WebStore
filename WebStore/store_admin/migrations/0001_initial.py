from django.db import models, migrations
from django.contrib.auth.models import Group

def create_groups(apps, schema_editor):
    Group.objects.get_or_create(name='Admin')
    Group.objects.get_or_create(name='Employee')

class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]