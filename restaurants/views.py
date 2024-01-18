from django.shortcuts import render
from .models import Food, Restaurant, Favorite, Category
from django.views.generic import ListView, DetailView

class HomeView(ListView):
    model = Restaurant
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['foods'] = Food.objects.all()
        context['favorites'] = Favorite.objects.all()
        context['categories'] = Category.objects.all()
        return context


class RestaurantsView(ListView):
    model = Restaurant
    template_name = 'restaurant_list.html'

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurant.html'


class FoodDetailView(DetailView):
    model = Food
    template_name = 'food.html'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category.html'


class FavoritesView(ListView):
    model = Favorite
    template_name = 'favorites.html'
