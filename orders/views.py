from django.shortcuts import render

from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.
from rest_framework import viewsets
from .models import Orders
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
# from users.permissions import IsEmpleado

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

        # if user.role != 'cliente':
        #     return Response({"detail": "Solo los clientes pueden ver sus pedidos."}, status=403)

        pedidos = Orders.objects.filter(client=user)
        serializer = self.get_serializer(pedidos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['put', 'patch'], url_path='set-status')
    def set_estado(self, request, pk=None):
        user = request.user

        if user.role != 'empleado':
            return Response({"detail": "Solo empleados pueden cambiar el estado."}, status=403)

        pedido = self.get_object()
        nuevo_estado = request.data.get("status")

        # CAMBIO: Aceptamos todos los estados del frontend
        # (Verificar que coincidan con los botones del BackOffice)
        valid_statuses = ['pending', 'ready to ship', 'shipped', 'delivered']


        # if nuevo_estado not in ['pending', 'delivered']:
        #     return Response({"error": "Estado inválido."}, status=400)

        if not nuevo_estado or nuevo_estado.lower() not in valid_statuses:
            return Response({"error": f"Estado inválido. Permitidos: {valid_statuses}"}, status=400)

        pedido.status = nuevo_estado.lower()
        pedido.employee = user  # quien lo está procesando
        pedido.save()

        return Response(self.get_serializer(pedido).data)