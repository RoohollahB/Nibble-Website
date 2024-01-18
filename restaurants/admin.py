from django.contrib import admin
from .models import Food, Restaurant, Favorite, Category


admin.site.register(Restaurant)
admin.site.register(Food)
admin.site.register(Favorite)
admin.site.register(Category)

