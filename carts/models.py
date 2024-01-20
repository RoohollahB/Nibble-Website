from django.db import models
from accounts.models import User
from restaurants.models import Food, Restaurant


class Discount(models.Model):
    code = models.CharField(max_length=10)
    value = models.IntegerField()
    type = models.CharField(max_length=10, choices=[('P', 'Percent'), ('A', 'Amount')])
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(null=True)
    limit = models.SmallIntegerField()
    description = models.TextField()


class Cart(models.Model):
    total_price = models.IntegerField()
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField()
    is_ordered = models.BooleanField(default=False)
    is_submited = models.BooleanField(default=False)
    delivery_code = models.CharField(max_length=5)


class CartItem(models.Model):
    food = models.ForeignKey(Food, on_delete=models.PROTECT)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    quantity = models.SmallIntegerField(default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
