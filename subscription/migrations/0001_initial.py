# Generated by Django 3.1 on 2020-08-22 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('started_at', models.TextField()),
                ('ended_at', models.TextField()),
                ('canceled_at', models.TextField()),
                ('status', models.CharField(max_length=50)),
                ('subscription_id', models.TextField()),
                ('product_id', models.TextField()),
                ('user_id', models.TextField()),
            ],
        ),
    ]
