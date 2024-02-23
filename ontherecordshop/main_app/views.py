from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

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

def signup(request):
    page_name = "Create Account"
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid credentials - Please try again.'
    form = UserCreationForm()
    context = {'form':form, 'error': error_message, 'page_name': page_name}
    return render(request, 'registration/signup.html', context)


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        # Update quantity if the item already exists in the cart
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()

        messages.success(request, f"{quantity} x {product.album} added to the cart.")

        return redirect('cart')

    return render(request, 'products/product_detail.html', {'product': product})

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart/view_cart.html', {'cart': cart, 'cart_items': cart_items})

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def update_cart_item(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))

        # Validate quantity
        if 1 <= quantity <= cart_item.product.stock:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f"Quantity updated for {cart_item.product.album}.")
        else:
            messages.error(request, "Invalid quantity.")

        return redirect('cart')

    return render(request, 'products/view_cart.html', {'cart_items': CartItem.objects.filter(cart=request.user.cart)})