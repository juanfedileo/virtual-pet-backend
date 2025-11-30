from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Opciones de Rol
    ROLE_CHOICES = (
        ('cliente', 'Cliente'),
        ('empleado', 'Empleado'),
    )
    
    # Opciones de Notificación (Referencia)
    NOTIFICATION_CHOICES = [
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('none', 'No avisar'),
    ]

    # Campos existentes
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='cliente')
    
    # Campos de contacto extra
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    # Campo de canales de notificación (JSON)
    notification_channels = models.JSONField(
        default=list, 
        blank=True,
        help_text="Lista de canales seleccionados, ej: ['email', 'whatsapp']"
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
