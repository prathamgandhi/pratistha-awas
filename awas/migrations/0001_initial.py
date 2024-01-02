# Generated by Django 5.0 on 2024-01-01 16:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest_name', models.TextField()),
                ('city', models.TextField(blank=True, null=True)),
                ('mobile_no', models.CharField(max_length=10)),
                ('ext_reg_no', models.IntegerField(blank=True, null=True)),
                ('remark', models.TextField(blank=True, null=True)),
                ('no_of_persons', models.IntegerField(blank=True, null=True)),
                ('arrival_date', models.DateTimeField(blank=True, null=True)),
                ('departure_date', models.DateTimeField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('language', models.TextField(blank=True, null=True)),
                ('state', models.TextField(blank=True, null=True)),
                ('country', models.TextField(blank=True, null=True)),
                ('mandal', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('transport', models.TextField(blank=True, null=True)),
                ('capacity', models.IntegerField(blank=True, null=True)),
                ('lock_no', models.TextField(blank=True, null=True)),
                ('awas_incharge', models.TextField(blank=True, null=True)),
                ('remark', models.TextField(blank=True, null=True)),
                ('checkin_time', models.TimeField(blank=True, null=True)),
                ('checkout_time', models.TimeField(blank=True, null=True)),
                ('map_link', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('persons_reserved', models.IntegerField()),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='awas.guest')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='awas.location')),
            ],
        ),
    ]
