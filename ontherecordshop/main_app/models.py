from django.db import models

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

    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.album