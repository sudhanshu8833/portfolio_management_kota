# Generated by Django 4.0.6 on 2022-10-18 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamanagement', '0011_user1_expiry_3_user1_working_days_3'),
    ]

    operations = [
        migrations.AddField(
            model_name='strategy',
            name='expiry_3',
            field=models.CharField(default='NA', max_length=12),
        ),
        migrations.AddField(
            model_name='strategy',
            name='working_days_3',
            field=models.IntegerField(default=0),
        ),
    ]
