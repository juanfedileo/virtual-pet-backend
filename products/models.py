from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    image = models.URLField(blank=True)  # URL de la imagen
    

    def __str__(self):
        return self.title