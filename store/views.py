from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import uuid

from .utils import cookie_cart, cart_data, guest_order


# Create your views here.


def store(request):
    data = cart_data(request)
    cart_items = data["cartItems"]

    products = Product.objects.all()
    context = {"products": products, 'cart_items': cart_items}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cookie_cart(request)
    cart_items = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {"items": items, 'order': order, 'cart_items': cart_items}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cookie_cart(request)
    cart_items = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {"items": items, 'order': order, 'cart_items': cart_items}
    return render(request, 'store/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    print('Action:', action, 'Product:', product_id)

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()
    return JsonResponse('Item was added', safe=False)


def process_order(request):
    transaction_id = uuid.uuid4()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guest_order(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data["shipping"]["address"],
            city=data["shipping"]["city"],
            zipcode=data["shipping"]["zipcode"]
        )

    return JsonResponse("Payment complete", safe=False)
