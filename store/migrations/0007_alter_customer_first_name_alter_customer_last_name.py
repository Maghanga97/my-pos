# Generated by Django 4.1.1 on 2023-02-12 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_returneditem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
