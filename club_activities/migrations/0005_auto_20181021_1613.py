# Generated by Django 2.1.1 on 2018-10-21 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('club_activities', '0004_auto_20181021_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='club',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='club_activities.Club'),
        ),
    ]