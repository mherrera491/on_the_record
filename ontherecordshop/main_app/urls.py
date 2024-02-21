from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("products/", views.products_index, name='all_products'),
    path("cart/", views.cart, name='cart'),
    path("checkout/", views.checkout, name='checkout'),
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),
]

