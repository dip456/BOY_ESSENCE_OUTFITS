# Generated by Django 5.0.4 on 2024-05-04 04:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_rename_customer_id_mycustomermodel_customer_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mycustomermodel',
            name='is_added_address',
        ),
    ]
