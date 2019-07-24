# Generated by Django 2.1.1 on 2019-06-28 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club_activities', '0017_auto_20181025_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='image',
            field=models.ImageField(null=True, upload_to='club_image'),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, upload_to='event_image'),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='images',
            field=models.ImageField(blank=True, upload_to='gallery'),
        ),
    ]