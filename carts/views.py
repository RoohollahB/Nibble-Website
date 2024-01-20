from django.shortcuts import render, redirect
from .models import Cart, CartItem, Discount, Order
from accounts.models import User
from restaurants.models import Food, Restaurant
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def view_cart(request):
    order = Order.objects.get(user=request.user, is_submited=False)
    cart_items = order.item_set.all()
    total_price = sum(item.food.price * item.quantity for item in cart_items)
    return render(request, 'cart/cart.html', {"cart_items": cart_items, "total_price": total_price})


@login_required
def add_to_cart(request):
    order, created = Order.objects.get_or_create(user=request.user, is_submited=False)
    if request.method == "POST":
        food_id = int(request.POST.get("food_id"))
        food = Food.objects.get(id=int(food_id))
        restaurant = food.restaurant
        if created:
            CartItem.objects.create(food=food, order=order, quantity=1, restaurant=restaurant)
        else:
            is_added = order.cartitem_set.filter(food=food).exists()
            if is_added:
                messages.info(request, "Food is already in cart")
            else:
                CartItem.objects.create(order=order, food=food, quantity=1, restaurant=restaurant)
                messages.info(request, "Food added successfully")

        # restaurant = food.restaurant
        # cart_item, created = CartItem.objects.get_or_create(food=food, user=request.user, restaurant=restaurant)
        # cart_item.quantity += 1
        # cart_item.save()
        return redirect('view_cart')


def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=int(item_id))
    cart_item.quantity -= 1
    if cart_item.quantity == 0:
        cart_item.delete()
    return redirect('view_cart')


def submit_order(request):
    if request.method == 'POST':
        order = Order.objects.get(is_submited=False)



class OrderDetailView(DetailView):
    model = Order


class OrderListView(ListView):
    template_name = 'order.html'
    model = Order
