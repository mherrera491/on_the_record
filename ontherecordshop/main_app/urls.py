from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("products/", views.products_index, name='all_products'),
    path("cart/", views.cart, name='cart'),
    path("checkout/", views.checkout, name='checkout'),
]

