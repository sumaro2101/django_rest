# Generated by Django 5.0.6 on 2024-07-05 11:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_subscribe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribe',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribe', to='courses.course', verbose_name='курс'),
        ),
    ]
