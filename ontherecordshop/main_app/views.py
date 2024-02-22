from django.shortcuts import render, redirect
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required

def home(request):
    page_name = "Home"
    return render(request, 'home.html', {'page_name': page_name})

def products_index(request):
    page_name = "Shop All"
    products = Product.objects.all()
    return render(request, 'products/index.html', { 'products': products, 'page_name': page_name })

def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'products/detail.html', { 'product': product })

def cart(request):
    return render(request, 'cart.html')

def checkout(request):
    return render(request, 'checkout.html')


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart/view_cart.html', {'cart': cart, 'cart_items': cart_items})