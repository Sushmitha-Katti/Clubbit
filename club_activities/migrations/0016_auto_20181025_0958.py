# Generated by Django 2.1.1 on 2018-10-25 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club_activities', '0015_auto_20181025_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club_request',
            name='desc',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
