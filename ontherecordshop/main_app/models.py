from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    album = models.CharField(max_length=250)
    artist = models.CharField(max_length=100, default='Unknown')
    release_date = models.DateField(null=True, default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    album_cover = models.URLField()
    stock = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.album
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f'Cart - {self.user.username}'
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.album} in {self.cart}'
    
    def get_absolute_url(self):
        return reverse('cart_item_delete', kwargs={'pk': self.pk})