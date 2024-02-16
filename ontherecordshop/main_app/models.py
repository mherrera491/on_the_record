from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField()
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title