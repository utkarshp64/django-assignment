# Generated by Django 3.1 on 2020-08-23 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0002_auto_20200823_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='price_id',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]