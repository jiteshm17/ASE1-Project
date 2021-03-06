# Generated by Django 2.1.3 on 2018-12-08 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0009_merge_20181208_1658'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='vendor',
            field=models.ManyToManyField(null=True, to='vendor.VendorProfile'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='vendor',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='vendor.VendorProfile'),
        ),
    ]
