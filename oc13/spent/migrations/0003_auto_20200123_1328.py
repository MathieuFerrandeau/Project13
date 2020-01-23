# Generated by Django 3.0.2 on 2020-01-23 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spent', '0002_auto_20200123_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outlay',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='outlay',
            name='payment_method',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
