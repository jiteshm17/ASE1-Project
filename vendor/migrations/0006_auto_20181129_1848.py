# Generated by Django 2.1.2 on 2018-11-29 13:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0005_auto_20181128_1254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendorqty',
            name='product',
        ),
        migrations.AddField(
            model_name='product',
            name='qty',
            field=models.ManyToManyField(to='vendor.VendorQty'),
        ),
        migrations.AlterField(
            model_name='vendorqty',
            name='Vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
