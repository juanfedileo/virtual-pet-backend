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
        
        valid_statuses = ['pending', 'ready to ship', 'shipped', 'delivered']
        if not nuevo_estado or nuevo_estado.lower() not in valid_statuses:
            return Response({"error": f"Estado inválido."}, status=400)

        pedido.status = nuevo_estado.lower()
        pedido.employee = user
        pedido.save()

        # --- LÓGICA DE NOTIFICACIÓN MEJORADA ---
        if pedido.status == 'shipped':
            if 'email' in pedido.notification_channels:
                destinatario = pedido.client.email
                if destinatario:
                    # 1. Preparar datos
                    nombre_cliente = pedido.shipping_name or pedido.client.first_name or "Cliente"
                    direccion = pedido.shipping_address or "Retiro en sucursal"
                    
                    # 2. Construir filas de la tabla de productos (HTML)
                    items_html_rows = ""
                    for item in pedido.orderitem_set.all():
                        total_item = item.quantity * item.price_at_purchase
                        items_html_rows += f"""
                        <tr style="border-bottom: 1px solid #eee;">
                            <td style="padding: 10px; color: #333;">{item.product.title}</td>
                            <td style="padding: 10px; text-align: center; color: #333;">{item.quantity}</td>
                            <td style="padding: 10px; text-align: right; color: #333;">${item.price_at_purchase}</td>
                        </tr>
                        """

                    # 3. Mensaje en Texto Plano (Limpio, sin indentación extra)
                    mensaje_plano = (
                        f"Hola {nombre_cliente}.\n"
                        f"Tu pedido #{pedido.id} ha sido enviado a {direccion}.\n"
                        f"Total: ${pedido.total}\n\n"
                        f"Gracias por elegir Virtual Pet."
                    )

                    # 4. Mensaje HTML (Diseño)
                    mensaje_html = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <style>
                            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                            .container {{ max-width: 600px; margin: 0 auto; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden; }}
                            .header {{ background-color: #005E97; padding: 20px; text-align: center; color: white; }}
                            .content {{ padding: 20px; }}
                            .info-box {{ background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
                            .footer {{ background-color: #f1f1f1; padding: 10px; text-align: center; font-size: 12px; color: #666; }}
                            table {{ width: 100%; border-collapse: collapse; }}
                            th {{ text-align: left; background-color: #f1f1f1; padding: 10px; }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <div class="header">
                                <h1 style="margin:0;">Virtual Pet 🐾</h1>
                            </div>
                            <div class="content">
                                <h2>¡Tu pedido está en camino! 🚚</h2>
                                <p>Hola <strong>{nombre_cliente}</strong>,</p>
                                <p>Tenemos excelentes noticias. Hemos despachado tus productos y ya van rumbo a tu hogar.</p>
                                
                                <div class="info-box">
                                    <strong>📍 Dirección de envío:</strong><br>
                                    {direccion}
                                </div>

                                <h3>Resumen del Pedido #{pedido.id}</h3>
                                <table>
                                    <thead>
                                        <tr>
                                            <th>Producto</th>
                                            <th style="text-align: center;">Cant.</th>
                                            <th style="text-align: right;">Precio</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {items_html_rows}
                                    </tbody>
                                    <tfoot>
                                        <tr>
                                            <td colspan="2" style="padding: 10px; text-align: right; font-weight: bold;">TOTAL:</td>
                                            <td style="padding: 10px; text-align: right; font-weight: bold; color: #005E97;">${pedido.total}</td>
                                        </tr>
                                    </tfoot>
                                </table>
                            </div>
                            <div class="footer">
                                <p>Gracias por confiar en nosotros.<br>El equipo de Virtual Pet</p>
                            </div>
                        </div>
                    </body>
                    </html>
                    """

                    print(f"📧 Enviando HTML mail a {destinatario}...")

                    try:
                        send_mail(
                            subject=f'📦 ¡Tu pedido #{pedido.id} está en camino!',
                            message=mensaje_plano, # Fallback para clientes viejos
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[destinatario],
                            html_message=mensaje_html, # 👈 AQUÍ VA EL HTML
                            fail_silently=False, 
                        )
                        print("✅ Correo enviado con éxito.")
                    except Exception as e:
                        print(f"❌ Error al enviar correo: {e}")

        return Response(self.get_serializer(pedido).data)
    # def set_estado(self, request, pk=None):
    #     user = request.user

    #     if user.role != 'empleado':
    #         return Response({"detail": "Solo empleados pueden cambiar el estado."}, status=403)

    #     pedido = self.get_object()
    #     nuevo_estado = request.data.get("status")

    #     # CAMBIO: Aceptamos todos los estados del frontend
    #     # (Verificar que coincidan con los botones del BackOffice)
    #     valid_statuses = ['pending', 'ready to ship', 'shipped', 'delivered']


    #     # if nuevo_estado not in ['pending', 'delivered']:
    #     #     return Response({"error": "Estado inválido."}, status=400)

    #     if not nuevo_estado or nuevo_estado.lower() not in valid_statuses:
    #         return Response({"error": f"Estado inválido. Permitidos: {valid_statuses}"}, status=400)

    #     pedido.status = nuevo_estado.lower()
    #     pedido.employee = user  # quien lo está procesando
    #     pedido.save()

    #     # 👇👇👇 AGREGA ESTO TEMPORALMENTE 👇👇👇
    #     print(f"\n--- 🕵️‍♂️ DEBUGGING VIRTUALPET ---")
    #     print(f"1. Estado recibido del Front: '{nuevo_estado}'")
    #     print(f"2. Estado final en DB: '{pedido.status}'")
    #     print(f"3. Canales de notifiación (Raw): {pedido.notification_channels}")
    #     print(f"4. Tipo de dato de canales: {type(pedido.notification_channels)}")
    #     print(f"5. ¿Es 'shipped'? {pedido.status == 'shipped'}")
    #     print(f"6. ¿Está 'email' en la lista? {'email' in pedido.notification_channels}")
    #     print(f"----------------------------------\n")
    #     # 👆👆👆 FIN DE LOS PRINTS 👆👆👆
    #     if pedido.status == "shipped":

    #         # Verificamos si el usuario quiere recibir notificaciones por mail
    #         # Importaciones para el mail
    #         if 'email' in pedido.notification_channels:
    #             destinatario = pedido.client.email
    #             if destinatario:
    #                 # 1. Construimos el Resumen del Pedido
    #                 items_list = ""
    #                 for item in pedido.orderitem_set.all():
    #                     items_list += f"- {item.quantity}x {item.product.title} (${item.price_at_purchase})\n"

    #                 # 2. Armamos el mensaje completo
    #                 asunto = f'📦 ¡Tu pedido #{pedido.id} está en camino!'
                    
    #                 mensaje = f"""
    #                 Estimado/a {pedido.shipping_name or pedido.client.first_name or pedido.client.username},

    #                 ¡Buenas noticias! Tu pedido de Virtual Pet ha sido despachado y está en viaje.

    #                 📍 Dirección de envío:
    #                 {pedido.shipping_address}

    #                 📝 Resumen del pedido:
    #                 {items_list}
                    
    #                 💰 Total: ${pedido.total}

    #                 Gracias por elegirnos.
    #                 El equipo de Virtual Pet.
    #                 """

    #                 print(f"📧 Enviando correo a {destinatario}...")

    #                 try:
    #                     send_mail(
    #                         subject=asunto,
    #                         message=mensaje,
    #                         from_email=settings.DEFAULT_FROM_EMAIL,
    #                         recipient_list=[destinatario],
    #                         fail_silently=False, 
    #                     )
    #                     print("✅ Correo enviado con éxito.")
    #                 except Exception as e:
    #                     print(f"❌ Error al enviar correo: {e}")

    #     return Response(self.get_serializer(pedido).data)