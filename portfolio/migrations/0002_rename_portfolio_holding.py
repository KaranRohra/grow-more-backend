# Generated by Django 4.1.1 on 2022-11-21 10:39

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("markets", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("portfolio", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Portfolio",
            new_name="Holding",
        ),
    ]