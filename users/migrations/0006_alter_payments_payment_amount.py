# Generated by Django 5.0.6 on 2024-06-28 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_payments_pay_course_alter_payments_pay_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='payment_amount',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=10, verbose_name='сумма оплаты'),
        ),
    ]