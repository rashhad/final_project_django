# Generated by Django 4.2.3 on 2023-09-05 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_profile_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='pro_pic',
            field=models.ImageField(null=True, upload_to='pro_pic'),
        ),
    ]
