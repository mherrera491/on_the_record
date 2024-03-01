from django.contrib import admin
from .models import Product, Genre, Cart, CartItem, Wishlist, WishlistItem

# Register your models here.
admin.site.register(Product)
admin.site.register(Genre)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(WishlistItem)
admin.site.register(Wishlist)