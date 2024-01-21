# Generated by Django 5.0.1 on 2024-01-21 04:11

import restaurants.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0002_category_icon_restaurant_featured'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=models.ImageField(default='images/category/default.png', upload_to=restaurants.models.get_category_image_filepath),
        ),
    ]
