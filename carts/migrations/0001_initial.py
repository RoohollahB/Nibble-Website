# Generated by Django 5.0.1 on 2024-01-20 19:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('restaurants', '0002_category_icon_restaurant_featured'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('value', models.IntegerField()),
                ('type', models.CharField(choices=[('P', 'Percent'), ('A', 'Amount')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expired_at', models.DateTimeField(null=True)),
                ('limit', models.SmallIntegerField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('discount', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='carts.discount')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_at', models.DateTimeField()),
                ('is_ordered', models.BooleanField(default=False)),
                ('is_submited', models.BooleanField(default=False)),
                ('delivery_code', models.CharField(max_length=5)),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='carts.cart')),
                ('discount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts.discount')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField(default=0)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restaurants.food')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restaurants.restaurant')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts.order')),
            ],
        ),
    ]
