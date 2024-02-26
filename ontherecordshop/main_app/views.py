from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView, TemplateView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.conf import settings
import os, stripe
from dotenv import load_dotenv
load_dotenv()

def home(request):
    page_name = "On The Record"
    featured_releases = Product.objects.filter(is_featured=True)[:4]
    new_releases = Product.objects.order_by('-release_date')[:4]
    return render(request, 'home.html', {'page_name': page_name, 'featured_releases': featured_releases, 'new_releases': new_releases})

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

    return render(request, 'products/detail.html', {'product': product})

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    subtotal = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'cart/view_cart.html', {'cart': cart, 'cart_items': cart_items, 'subtotal': subtotal})

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
            messages.success(request, f"Quantity Updated For - {cart_item.product.album}.")
        else:
            messages.error(request, "Invalid Quantity.")

        return redirect('cart')

    return render(request, 'products/view_cart.html', {'cart_items': CartItem.objects.filter(cart=request.user.cart)})



def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        products_to_update = []
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.album,
                    },
                    'unit_amount': int(item.product.price * 100),
                },
                'quantity': item.quantity,
            } for item in cart_items],
            mode='payment',
            success_url=request.build_absolute_uri(reverse("success")),
            cancel_url=request.build_absolute_uri(reverse("cancel")), 
        )

        for item in cart_items:
            product = item.product
            product.stock -= item.quantity
            products_to_update.append(product)
        
        Product.objects.bulk_update(products_to_update, ['stock'])

        return redirect(checkout_session.url, code=303)

    return render(request, 'cart/view_cart.html', {'cart': cart, 'cart_items': cart_items, 'subtotal': subtotal})


class SuccessView(TemplateView):
    template_name='cart/success.html'

    def get(self, request):

        user_cart, created = Cart.objects.get_or_create(user=request.user)
        user_cart.products.clear()

        return render(request, self.template_name)

class CancelView(TemplateView):
    template_name='cart/cancel.html'