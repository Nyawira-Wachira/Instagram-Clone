# Generated by Django 4.0.5 on 2022-06-06 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0006_alter_profile_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(max_length=300),
        ),
    ]
