from django.urls import path
from . import views


urlpatterns = [
    path('/order-list/', views.OrderListView.as_view(), name='order_list'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart')
]