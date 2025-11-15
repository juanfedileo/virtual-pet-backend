from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Orders
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsEmpleado

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        # Solo los empleados pueden hacer GET (listar o ver órdenes)
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsEmpleado]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]