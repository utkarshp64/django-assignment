# Generated by Django 3.1 on 2020-08-23 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='canceled_at',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='ended_at',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='started_at',
            field=models.TextField(null=True),
        ),
    ]