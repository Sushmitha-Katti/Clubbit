# Generated by Django 2.1.1 on 2018-10-23 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club_activities', '0007_event_popular'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='popular',
            field=models.IntegerField(choices=[(1, 'Add_In_front'), (0, 'Dont_add')], default=0),
        ),
    ]
