# Generated by Django 2.1.3 on 2018-12-08 15:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_auto_20181208_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='vendor',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='vendor',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]