# Generated by Django 4.2.3 on 2023-09-03 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_posts_slug_topic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='slug_topic',
        ),
    ]
