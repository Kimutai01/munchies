# Generated by Django 4.2.4 on 2023-08-16 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cover_picture',
            field=models.ImageField(blank=True, default='profiles/default-cover.png', null=True, upload_to='profiles/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profiles/default-user.png', null=True, upload_to='profiles/'),
        ),
    ]
