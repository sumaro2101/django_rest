# Generated by Django 5.0.6 on 2024-06-28 14:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_lesson_course'),
        ('users', '0003_alter_user_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_pay', models.DateTimeField(auto_now_add=True, verbose_name='Дата платежа')),
                ('payment_amount', models.PositiveIntegerField(editable=False, verbose_name='сумма оплаты')),
                ('payment_method', models.CharField(choices=[('cash', 'наличные'), ('modey_transfer', 'перевод денег')], max_length=50, verbose_name='способ оплаты')),
                ('pay_course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='courses.course', verbose_name='платеж курса')),
                ('pay_lesson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='courses.lesson', verbose_name='платеж урока')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
        ),
    ]
