from django.db import models
from django.conf import settings
from products.models import Product

class Orders(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('ready to ship', 'Ready to ship'), 
        ('shipped', 'Shipped'),             
        ('delivered', 'Delivered'),
    ]

    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_orders'
    )
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employee_orders'
    )
    
    # --- CAMBIO PRINCIPAL ---
    # Ya no definimos la relación directamente.
    # Usamos 'through' para apuntar a nuestro nuevo modelo 'OrderItem'.
    products = models.ManyToManyField(
        Product, 
        through='OrderItem',  # <- Aquí está la magia
        related_name='orders'
    )
    # --- FIN DEL CAMBIO ---

    shipping_address = models.CharField(max_length=255, blank=True, null=True)
    shipping_name = models.CharField(max_length=150, blank=True, null=True) # El nombre/username
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.client.username} ({self.status})"
    
    # Opcional: una propiedad para calcular el total del pedido
    @property
    def total(self):
        return self.orderitem_set.aggregate(
            total=models.Sum(models.F('quantity') * models.F('price_at_purchase'))
        )['total'] or 0


# --- MODELO NUEVO ---
# Este es nuestro modelo "intermedio"
class OrderItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT) # PROTECT evita borrar un producto si está en un pedido
    
    # ¡El campo que necesitábamos!
    quantity = models.PositiveIntegerField(default=1) 
    
    # ¡La mejora recomendada!
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        # Asegura que no podamos añadir el mismo producto dos veces en el mismo pedido
        unique_together = ('order', 'product')

    def save(self, *args, **kwargs):
        # Guarda automáticamente el precio del producto al crear el item
        if self.pk is None and self.price_at_purchase is None:
            # Asumimos que tu modelo Product tiene un campo 'price'
            # (Si se llama distinto, ajústalo)
            self.price_at_purchase = self.product.price 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.title} in Order #{self.order.id}"


# from django.db import models

# # Create your models here.
# from django.db import models
# from django.conf import settings
# from products.models import Product

# class Orders(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('delivered', 'Delivered'),
#     ]

#     id = models.AutoField(primary_key=True)
#     client = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='client_orders'
#     )
#     employee = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='employee_orders'
#     )
#     products = models.ManyToManyField(Product, related_name='orders')
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Order #{self.id} - {self.client.username} ({self.status})"
