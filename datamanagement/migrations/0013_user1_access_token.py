# Generated by Django 4.0.6 on 2022-11-09 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamanagement', '0012_strategy_expiry_3_strategy_working_days_3'),
    ]

    operations = [
        migrations.AddField(
            model_name='user1',
            name='access_token',
            field=models.CharField(default='NA', max_length=1000),
        ),
    ]
