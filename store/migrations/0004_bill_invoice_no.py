# Generated by Django 4.1.1 on 2023-02-11 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_remove_bill_bill_total_remove_bill_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='invoice_no',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
