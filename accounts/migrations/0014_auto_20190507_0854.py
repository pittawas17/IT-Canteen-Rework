# Generated by Django 2.2 on 2019-05-07 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20190506_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='menu',
            field=models.TextField(default='some menu'),
        ),
        migrations.AddField(
            model_name='history',
            name='order_datetime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='history',
            name='shop',
            field=models.TextField(default='some shop'),
        ),
    ]