# Generated by Django 2.1.4 on 2019-04-11 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CountingLog', '0007_pipeline'),
    ]

    operations = [
        migrations.AddField(
            model_name='pipeline',
            name='pipelineClosed',
            field=models.BooleanField(default=False),
        ),
    ]
