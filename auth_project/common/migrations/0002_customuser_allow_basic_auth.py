# Generated by Django 3.1.2 on 2020-10-24 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='allow_basic_auth',
            field=models.BooleanField(default=False),
        ),
    ]
