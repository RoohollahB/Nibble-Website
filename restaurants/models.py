from django.db import models
from accounts.models import User


def get_restaurant_image_filepath(self, filename):
    return f'images/restaurants/{str(self.name)}/{str(filename)}'


def get_default_restaurant_image_filepath():
    return f'images/restaurant_default.png'


def get_food_image_filepath(self, filename):
    return f'images/food/{self.restaurant}/{self.name}/{str(filename)}'


def get_default_food_image_filepath():
    return f'images/food_default.png'


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    delivery_cost = models.PositiveIntegerField()
    opening_hours = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_restaurant_image_filepath,
                              default=get_default_restaurant_image_filepath)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_food_image_filepath,
                              default=get_default_food_image_filepath)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)

