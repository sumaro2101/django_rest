# Generated by Django 5.0.6 on 2024-07-05 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_alter_subscribe_course'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['-time_update'], 'verbose_name': 'курс', 'verbose_name_plural': 'курсы'},
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ['-time_update'], 'verbose_name': 'урок', 'verbose_name_plural': 'уроки'},
        ),
        migrations.AddField(
            model_name='course',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='дата создания'),
        ),
        migrations.AddField(
            model_name='course',
            name='time_update',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='дата изменения'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='дата создания'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='time_update',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='дата изменения'),
        ),
    ]
