# Generated by Django 2.0.3 on 2018-11-13 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CountLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EmployeName', models.CharField(max_length=50, verbose_name='Employee Name')),
                ('DateCount', models.DateField(blank=True, null=True, verbose_name='Date of Count')),
                ('LotNo', models.CharField(max_length=20, verbose_name='Lot Number')),
                ('Quantity', models.IntegerField()),
                ('SupposedQuantity', models.FloatField(blank=True, null=True)),
                ('ScrapAllowance', models.FloatField(blank=True, null=True)),
                ('PreviousCount', models.FloatField(blank=True, null=True)),
                ('GlobalRank', models.IntegerField(blank=True, null=True, verbose_name='Global Rank')),
                ('MoveTo', models.CharField(blank=True, max_length=50, null=True, verbose_name='Move To Location')),
                ('ArrivedTo', models.BooleanField(default=False)),
                ('MissedClockOut', models.BooleanField(default=False, verbose_name='Missed Clock Out (Yes if Missed)')),
            ],
        ),
        migrations.CreateModel(
            name='ResourceLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PortEntry', models.CharField(max_length=50)),
                ('ResourceID', models.CharField(max_length=30)),
            ],
        ),
    ]