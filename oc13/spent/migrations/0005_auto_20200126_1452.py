# Generated by Django 3.0.2 on 2020-01-26 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spent', '0004_auto_20200126_1447'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useroutlay',
            name='outlay_field',
        ),
        migrations.AddField(
            model_name='useroutlay',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='useroutlay',
            name='creation_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='useroutlay',
            name='outlay',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='spent.Outlay'),
        ),
        migrations.AddField(
            model_name='useroutlay',
            name='payment_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='useroutlay',
            name='payment_method',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.DeleteModel(
            name='OutlayField',
        ),
    ]
