# Generated by Django 2.2 on 2019-05-04 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20190503_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='type',
            field=models.CharField(choices=[('01', 'customer'), ('02', 'shop')], default='01', max_length=2),
        ),
    ]
