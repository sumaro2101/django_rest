# Generated by Django 5.0.6 on 2024-06-26 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='video_link',
            field=models.FileField(blank=True, max_length=256, null=True, upload_to='courses/videos/%Y/%m/%d/', verbose_name='ссылка на видео'),
        ),
    ]
