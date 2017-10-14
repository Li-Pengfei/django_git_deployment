# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-14 23:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('EL', 'Electronics'), ('FA', 'Fashion & Accessories'), ('HA', 'Home & Appliances'), ('HB', 'Health & Beauty'), ('BT', 'Baby & Toy'), ('SO', 'Sports & Outdoors'), ('GC', 'Groceries'), ('OT', 'Others')], max_length=64)),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField(max_length=1024)),
                ('estimate_price', models.PositiveIntegerField()),
                ('exchange_address', models.TextField(max_length=256)),
                ('item_pic', models.URLField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_type', models.CharField(choices=[('CS', 'Cash'), ('EX', 'Exchange')], max_length=3)),
                ('offer_status', models.CharField(choices=[('ON', 'Active'), ('FI', 'Finished'), ('CA', 'Canceled')], max_length=3)),
                ('initiator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='offered', to='mainApp.ItemModel')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wanted', to='mainApp.ItemModel')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfileInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wechat', models.CharField(max_length=128)),
                ('profile_pic', models.ImageField(blank=True, upload_to='profile_pics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
