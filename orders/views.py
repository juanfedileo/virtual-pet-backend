from django.shortcuts import render

from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.
from rest_framework import viewsets
from .models import Orders
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsEmpleado

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user.role != 'empleado':
            return Response({"detail": "Solo empleados pueden ver todos los pedidos."}, status=403)

        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='my-orders')
    def mis_pedidos(self, request):
        user = request.user

        if user.role != 'cliente':
            return Response({"detail": "Solo los clientes pueden ver sus pedidos."}, status=403)

        pedidos = Orders.objects.filter(client=user)
        serializer = self.get_serializer(pedidos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['put'], url_path='set-state')
    def set_estado(self, request, pk=None):
        user = request.user

        if user.role != 'empleado':
            return Response({"detail": "Solo empleados pueden cambiar el estado."}, status=403)

        pedido = self.get_object()
        nuevo_estado = request.data.get("status")

        if nuevo_estado not in ['pending', 'delivered']:
            return Response({"error": "Estado inválido."}, status=400)

        pedido.status = nuevo_estado
        pedido.employee = user  # quien lo está procesando
        pedido.save()

        return Response(self.get_serializer(pedido).data)