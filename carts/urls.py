from django.urls import path
from . import views


urlpatterns = [
    path('/order-list/', views.OrderListView.as_view(), name='order_list')
]