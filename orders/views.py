from django.shortcuts import render

from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.
from rest_framework import viewsets
from .models import Orders
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
# Importaciones para el mail
from django.core.mail import send_mail
from django.conf import settings

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
        # rehabilitado en refactor
        if user.role != 'cliente':
            return Response({"detail": "Solo los clientes pueden ver sus pedidos."}, status=403)

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

        # 👇👇👇 AGREGA ESTO TEMPORALMENTE 👇👇👇
        print(f"\n--- 🕵️‍♂️ DEBUGGING VIRTUALPET ---")
        print(f"1. Estado recibido del Front: '{nuevo_estado}'")
        print(f"2. Estado final en DB: '{pedido.status}'")
        print(f"3. Canales de notifiación (Raw): {pedido.notification_channels}")
        print(f"4. Tipo de dato de canales: {type(pedido.notification_channels)}")
        print(f"5. ¿Es 'shipped'? {pedido.status == 'shipped'}")
        print(f"6. ¿Está 'email' en la lista? {'email' in pedido.notification_channels}")
        print(f"----------------------------------\n")
        # 👆👆👆 FIN DE LOS PRINTS 👆👆👆
        if pedido.status == "shipped":

            # Verificamos si el usuario quiere recibir notificaciones por mail
            # Importaciones para el mail
            if 'email' in pedido.notification_channels:
                destinatario = pedido.client.email
                if destinatario:
                    # 1. Construimos el Resumen del Pedido
                    items_list = ""
                    for item in pedido.orderitem_set.all():
                        items_list += f"- {item.quantity}x {item.product.title} (${item.price_at_purchase})\n"

                    # 2. Armamos el mensaje completo
                    asunto = f'📦 ¡Tu pedido #{pedido.id} está en camino!'
                    
                    mensaje = f"""
                    Estimado/a {pedido.shipping_name or pedido.client.first_name or pedido.client.username},

                    ¡Buenas noticias! Tu pedido de Virtual Pet ha sido despachado y está en viaje.

                    📍 Dirección de envío:
                    {pedido.shipping_address}

                    📝 Resumen del pedido:
                    {items_list}
                    
                    💰 Total: ${pedido.total}

                    Gracias por elegirnos.
                    El equipo de Virtual Pet.
                    """

                    print(f"📧 Enviando correo a {destinatario}...")

                    try:
                        send_mail(
                            subject=asunto,
                            message=mensaje,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[destinatario],
                            fail_silently=False, 
                        )
                        print("✅ Correo enviado con éxito.")
                    except Exception as e:
                        print(f"❌ Error al enviar correo: {e}")

        return Response(self.get_serializer(pedido).data)