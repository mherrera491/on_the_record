from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("products/", views.products_index, name='all_products'),
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('products/<int:pk>/', views.product_detail, name='detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='cart'),
]

