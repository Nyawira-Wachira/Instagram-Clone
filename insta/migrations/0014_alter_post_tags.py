# Generated by Django 4.0.5 on 2022-06-07 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0013_alter_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(null=True, related_name='tags', to='insta.tag'),
        ),
    ]
