# Generated by Django 5.0.6 on 2024-06-28 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_payments_payment_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'наличные'), ('money_transfer', 'перевод денег')], max_length=50, verbose_name='способ оплаты'),
        ),
    ]
