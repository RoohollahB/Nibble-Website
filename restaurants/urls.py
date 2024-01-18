from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('restaurants/', views.RestaurantsView.as_view(), name='restaurants'),
    path('restaurants/<int:pk>/', views.RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('foods/<int:pk>/', views.FoodDetailView.as_view(), name='food_detail'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('favorites', views.FavoritesView.as_view(), name='favorites')

]