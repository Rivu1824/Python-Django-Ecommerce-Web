# Generated by Django 5.0.1 on 2024-01-25 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bluewatermarines', '0004_alter_product_size_alter_product_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='Country',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='Postcode_Zip',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='State',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='Street_Address',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
