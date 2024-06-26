# Generated by Django 5.0.1 on 2024-01-25 16:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bluewatermarines', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThirdCategorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='Media/ThirdCategorie/Img')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('slug', models.SlugField(blank=True, default='', max_length=500, null=True)),
                ('parent_subcategorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bluewatermarines.subcategorie')),
            ],
            options={
                'verbose_name_plural': '04. ThirdCategories',
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bluewatermarines.thirdcategorie'),
        ),
    ]
