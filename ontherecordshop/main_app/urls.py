from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import update_cart_item, SuccessView, CancelView, genre_list, products_by_genre, products_by_artist, artist_list

urlpatterns = [
    path("", views.home, name='home'),
    path("products/", views.products_index, name='all_products'),
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('products/<int:pk>/', views.product_detail, name='detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart_item/<int:cart_item_id>/', update_cart_item, name='update_cart_item'),
    path('accounts/signup/', views.signup, name='signup'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('checkout/', views.checkout, name='checkout'),
    path('genres/', genre_list, name='genre_list'),
    path('genres/<int:genre_id>/', products_by_genre, name='products_by_genre'),
    path('artists/', artist_list, name='artist_list'),
    path('artists/<str:artist_name>/', products_by_artist, name="products_by_artist"),
]

