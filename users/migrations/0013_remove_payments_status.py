# Generated by Django 5.0.6 on 2024-07-08 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_payments_id_session'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payments',
            name='status',
        ),
    ]
