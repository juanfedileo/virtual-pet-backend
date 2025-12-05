from rest_framework import serializers
from .models import Orders, OrderItem  # <-- 1. Importamos el nuevo OrderItem
from products.models import Product
from products.serializers import ProductSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
# Opcional: Para mostrar datos del cliente, pero no es necesario aún
# from users.serializers import UserSerializer 

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Personalizamos la respuesta del Login para que devuelva
    todos los datos del usuario junto con el token.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Agregamos info extra al token encriptado
        token['role'] = user.role
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Esto es el JSON que recibe el frontend al loguearse
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'role': self.user.role,
            'address': self.user.address,
            'phone': self.user.phone,
            'notification_channels': self.user.notification_channels,
        }
        return data

class UserSerializer(serializers.ModelSerializer):
    """
    Se encarga de validar y crear nuevos usuarios (Registro).
    """
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(required=False) 

    class Meta:
        model = User
        # 👇 AQUÍ DEFINIMOS QUÉ CAMPOS SE ACEPTAN Y SE MUESTRAN
        fields = [
            "id", 
            "username", 
            "email", 
            "password", 
            "role", 
            "address", 
            "phone", 
            "first_name", 
            "last_name", 
            "notification_channels", 
            "is_staff", 
            "is_active"
        ]

    def create(self, validated_data):
        """
        Función que se ejecuta al guardar (POST).
        Aquí mapeamos los datos validados a las columnas de la DB.
        """
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
            role=validated_data.get('role', 'cliente'),
            
            # 👇 DATOS EXTRA (Si no vienen, guardamos string vacío)
            address=validated_data.get('address', ''),
            phone=validated_data.get('phone', ''),
            
            # 👇 AQUÍ SE GUARDAN EL NOMBRE Y APELLIDO
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            
            # 👇 AQUÍ SE GUARDA LA LISTA DE CANALES (['email', 'whatsapp'])
            notification_channels=validated_data.get('notification_channels', [])
        )
        return user
       
# --- 2. SERIALIZADOR NUEVO ---
# Este es un "serializador anidado" para los items.
# Define la forma que esperamos en el JSON: {'product_id': 1, 'quantity': 2}
class OrderItemPayloadSerializer(serializers.Serializer):
    # Usamos product_id para que coincida con el frontend, pero lo validamos
    # como un PrimaryKeyRelatedField que apunta al modelo Product.
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        # No usamos 'source' porque el frontend enviará 'product_id'
    )
    quantity = serializers.IntegerField(min_value=1)


# --- 2. SERIALIZADOR NUEVO (PARA LEER) ---
# Este serializer define CÓMO se debe VER un OrderItem
# cuando lo devolvemos en el JSON
class OrderItemReadSerializer(serializers.ModelSerializer):
    # 'product' será un objeto JSON completo (id, title, price, etc.)
    product = ProductSerializer(read_only=True) 

    class Meta:
        model = OrderItem
        # Le decimos qué campos mostrar
        fields = ['product', 'quantity', 'price_at_purchase']


class OrderSerializer(serializers.ModelSerializer):
    
    # --- 3. CAMPO NUEVO (para escribir) ---
    # Este es el campo que recibirá el array de items del frontend.
    # Lo marcamos como "write_only" porque no es un campo real
    # en el modelo 'Orders', solo lo usamos para crear.
    items = OrderItemPayloadSerializer(many=True, write_only=True)

    items_read = OrderItemReadSerializer(
        source='orderitem_set', 
        many=True, 
        read_only=True
    )

    # --- 4. CAMPO ANTIGUO (modificado para leer) ---
    # El campo 'products' (de ManyToManyField) ahora solo
    # lo usamos para "leer" los IDs de productos.
    products = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True  # <-- Marcado como solo lectura
    )
    
    # --- 5. CAMPO NUEVO (para leer) ---
    # (Opcional) Esto expone la propiedad @property 'total'
    # que agregamos a tu models.py
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    client_phone = serializers.CharField(source='client.phone', read_only=True)

    class Meta:
        model = Orders
        # 'items' se agrega a los fields para que sea aceptado en el POST
        fields = ['id', 'client', 'employee', 'products', 'items', 'status', 'created_at', 'total', 
        'items_read', 'shipping_address', 'shipping_name',  'notification_channels',
            'client_phone']
        
        # Ocultamos 'items' de la respuesta (GET) porque 'products' ya está ahí.
        extra_kwargs = {
            'items': {'write_only': True},
            'shipping_address': {'required': False}, 
            'shipping_name': {'required': False},
        }

    def validate(self, data):
        client = data.get('client')
        employee = data.get('employee')  # employee puede ser None

        if not client or client.role != 'cliente':
            raise serializers.ValidationError({"client": "Se debe asignar un cliente con el rol 'cliente'."})

        # --- 6. ARREGLO DEL BUG ---
        # Solo validamos el rol del empleado SI se proporcionó un empleado.
        if employee and employee.role != 'empleado':
            raise serializers.ValidationError({"employee": "El usuario asignado como empleado no tiene el rol 'empleado'."})

        if not data.get('items'):
            raise serializers.ValidationError({"items": "No se puede crear un pedido sin productos."})

        return data

    # --- 7. CAMBIO MÁS IMPORTANTE ---
    # Sobrescribimos el método create() para manejar los 'items' anidados.
    def create(self, validated_data):
        # 1. Sacamos los datos de los 'items' antes de crear la orden
        items_data = validated_data.pop('items')
        
        client = validated_data.get('client')

        if 'shipping_address' not in validated_data and client.address:
            validated_data['shipping_address'] = client.address

        if 'shipping_name' not in validated_data:
            # Usamos el nombre y apellido si existen, sino el username
            full_name = f"{client.first_name} {client.last_name}".strip()
            validated_data['shipping_name'] = full_name if full_name else client.username

        if 'notification_channels' not in validated_data:
            # Esto copia la lista completa (ej: ['email', 'whatsapp'])
            validated_data['notification_channels'] = client.notification_channels

            
        # 2. Creamos la Orden principal (con client, employee, etc.)
        order = Orders.objects.create(**validated_data)

        # 3. Iteramos sobre los items y creamos los OrderItem
        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                product=item_data['product_id'],  # 'product_id' ya es un objeto Product gracias al serializer
                quantity=item_data['quantity']
                # El 'price_at_purchase' se guarda automáticamente
                # gracias a la lógica en models.py
            )

        return order

# from rest_framework import serializers
# from .models import Orders
# from products.models import Product

# class OrderSerializer(serializers.ModelSerializer):
#     products = serializers.PrimaryKeyRelatedField(
#         many=True,
#         queryset=Product.objects.all()
#     )

#     class Meta:
#         model = Orders
#         fields = ['id', 'client', 'employee', 'products', 'status', 'created_at']
    
#     def validate(self, data):
#         client = data.get('client')
#         employee = data.get('employee')

#         if client.role != 'cliente':
#             raise serializers.ValidationError({"client": "El usuario asignado como cliente no tiene el rol 'cliente'."})

#         if employee.role != 'empleado':
#             raise serializers.ValidationError({"employee": "El usuario asignado como empleado no tiene el rol 'empleado'."})

#         return data