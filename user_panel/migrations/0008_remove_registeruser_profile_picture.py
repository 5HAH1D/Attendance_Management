# Generated by Django 4.2.1 on 2023-06-03 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_panel', '0007_alter_registeruser_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registeruser',
            name='profile_picture',
        ),
    ]