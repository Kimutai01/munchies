# Generated by Django 4.2.4 on 2023-08-17 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_vendor_vendor_license'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vendor',
            old_name='user_profile',
            new_name='profile',
        ),
    ]