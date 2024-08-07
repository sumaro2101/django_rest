# Generated by Django 5.0.6 on 2024-07-06 18:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_alter_course_options_alter_lesson_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_name',
            field=models.CharField(help_text='Имя курса', max_length=200, verbose_name='имя курса'),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_preview',
            field=models.ImageField(blank=True, help_text='Изображение характерезуещее курс', null=True, upload_to='courses/course/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.TextField(blank=True, help_text='Описание курса', null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='owner',
            field=models.ForeignKey(blank=True, help_text='Создатель курса', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец'),
        ),
        migrations.AlterField(
            model_name='course',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True, help_text='Дата создания, назначается автоматически', null=True, verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='course',
            name='time_update',
            field=models.DateTimeField(auto_now=True, help_text='Дата изменения, назначается автоматически', null=True, verbose_name='дата изменения'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(help_text='Курс урока', on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='courses.course', verbose_name='курс'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='description',
            field=models.TextField(blank=True, help_text='Описание урока', null=True, verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='lesson_name',
            field=models.CharField(help_text='Название урока, не более 200 символов', max_length=200, verbose_name='название урока'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='lesson_preview',
            field=models.ImageField(blank=True, help_text='Изображение характеризующее урок', null=True, upload_to='courses/lessons/%Y/%m/%d/', verbose_name='картинка'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='owner',
            field=models.ForeignKey(blank=True, help_text='Создатель урока', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True, help_text='Дата создания, назначается автоматически', null=True, verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='time_update',
            field=models.DateTimeField(auto_now=True, help_text='Дата изменения, назначается автоматически', null=True, verbose_name='дата изменения'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='video_link',
            field=models.CharField(help_text='Ссылка на видео урок', max_length=256, verbose_name='ссылка на видео урок'),
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='course',
            field=models.ForeignKey(help_text='Курс подписки', on_delete=django.db.models.deletion.CASCADE, related_name='subscribe', to='courses.course', verbose_name='курс'),
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='user',
            field=models.ForeignKey(help_text='Подписчик', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
    ]
