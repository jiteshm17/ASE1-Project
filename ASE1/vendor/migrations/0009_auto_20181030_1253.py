# Generated by Django 2.1.2 on 2018-10-30 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0008_auto_20181028_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
